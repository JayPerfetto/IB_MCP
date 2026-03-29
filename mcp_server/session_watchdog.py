"""
Background poll of IBKR gateway auth status; optional ssodh/init + reauthenticate recovery.

Does not replace /tickle (handled in api_gateway). Helps surface de-auth and sometimes
reopens a brokerage session when connected=true but authenticated=false.
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Optional

import httpx

from mcp_server.config import (
    BASE_URL,
    SESSION_WATCHDOG_ENABLED,
    SESSION_WATCHDOG_INTERVAL_SECONDS,
    SESSION_WATCHDOG_RECOVERY_COOLDOWN_SECONDS,
    SESSION_WATCHDOG_TRY_REAUTHENTICATE,
    SESSION_WATCHDOG_TRY_SSODH_INIT,
)

logger = logging.getLogger(__name__)


def _ensure_watchdog_logs_to_stderr() -> None:
    """INFO lines were invisible in Docker: root logger defaults to WARNING."""
    if logger.handlers:
        return
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("[session_watchdog] %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


def _parse_auth_payload(data: Any) -> tuple[Optional[bool], Optional[bool]]:
    """Return (connected, authenticated) from /iserver/auth/status JSON, if present."""
    if not isinstance(data, dict):
        return None, None
    connected = data.get("connected")
    if connected is None:
        connected = data.get("Connected")
    authenticated = data.get("authenticated")
    if authenticated is None:
        authenticated = data.get("Authenticated")
    return connected, authenticated


async def _fetch_auth_status(client: httpx.AsyncClient) -> tuple[Optional[bool], Optional[bool], Optional[int]]:
    try:
        r = await client.get(f"{BASE_URL}/iserver/auth/status", timeout=15.0)
        if r.status_code >= 400:
            logger.warning(
                "session_watchdog: auth/status HTTP %s — %s",
                r.status_code,
                (r.text or "")[:200],
            )
            return None, None, r.status_code
        data = r.json()
        c, a = _parse_auth_payload(data)
        return c, a, r.status_code
    except httpx.RequestError as exc:
        logger.warning("session_watchdog: auth/status request failed: %s", exc)
        return None, None, None
    except ValueError:
        logger.warning("session_watchdog: auth/status returned non-JSON")
        return None, None, None


async def _post_recovery(client: httpx.AsyncClient, path: str, label: str) -> bool:
    url = f"{BASE_URL}{path}"
    try:
        r = await client.post(url, json={}, timeout=15.0)
        text = (r.text or "")[:300]
        if r.status_code < 400:
            logger.info("session_watchdog: %s OK (HTTP %s) %s", label, r.status_code, text)
            return True
        logger.warning("session_watchdog: %s HTTP %s %s", label, r.status_code, text)
        return False
    except httpx.RequestError as exc:
        logger.warning("session_watchdog: %s failed: %s", label, exc)
        return False


async def session_watchdog_loop() -> None:
    _ensure_watchdog_logs_to_stderr()
    interval = max(15, SESSION_WATCHDOG_INTERVAL_SECONDS)
    cooldown = max(60, SESSION_WATCHDOG_RECOVERY_COOLDOWN_SECONDS)
    last_recovery_mono: float = 0.0
    prev_authenticated: Optional[bool] = None

    logger.info(
        "session_watchdog: started (interval=%ss, ssodh_init=%s, reauthenticate=%s, cooldown=%ss)",
        interval,
        SESSION_WATCHDOG_TRY_SSODH_INIT,
        SESSION_WATCHDOG_TRY_REAUTHENTICATE,
        cooldown,
    )

    async with httpx.AsyncClient(verify=False) as client:
        while True:
            try:
                connected, authenticated, _ = await _fetch_auth_status(client)

                if authenticated is not None and authenticated != prev_authenticated:
                    if authenticated:
                        logger.info("session_watchdog: brokerage session authenticated (connected=%s)", connected)
                    else:
                        logger.warning(
                            "session_watchdog: brokerage session not authenticated (connected=%s) — "
                            "you may need Client Portal browser login if recovery fails",
                            connected,
                        )
                    prev_authenticated = authenticated

                if (
                    connected is True
                    and authenticated is False
                    and (SESSION_WATCHDOG_TRY_SSODH_INIT or SESSION_WATCHDOG_TRY_REAUTHENTICATE)
                ):
                    now = time.monotonic()
                    if now - last_recovery_mono >= cooldown:
                        last_recovery_mono = now
                        logger.info("session_watchdog: attempting recovery (connected but not authenticated)")
                        if SESSION_WATCHDOG_TRY_SSODH_INIT:
                            await _post_recovery(
                                client,
                                "/iserver/auth/ssodh/init",
                                "ssodh/init",
                            )
                        if SESSION_WATCHDOG_TRY_REAUTHENTICATE:
                            await _post_recovery(client, "/iserver/reauthenticate", "reauthenticate")
                        _, after, _ = await _fetch_auth_status(client)
                        if after is True:
                            logger.info("session_watchdog: recovery succeeded (authenticated=true)")
                            prev_authenticated = True
                        elif after is False:
                            logger.warning("session_watchdog: recovery did not restore authenticated=true")
                            prev_authenticated = False

                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                logger.info("session_watchdog: stopped")
                raise
