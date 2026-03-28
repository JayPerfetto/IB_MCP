# watchlists.py
from fastapi import APIRouter, Body, Query
from typing import Any, Dict, List, Optional

import httpx
from pydantic import BaseModel, Field

from mcp_server.config import BASE_URL

router = APIRouter()


class WatchlistRow(BaseModel):
    """Row object as IBKR expects for POST /iserver/watchlist."""

    C: str = Field(..., description="Contract ID (conid) as a string.")


class WatchlistCreateRequest(BaseModel):
    """Body for POST /iserver/watchlist (create or replace)."""

    id: str = Field(
        ...,
        description="Numeric string watchlist id, unique among your lists (digits 0-9 per IBKR).",
    )
    name: str = Field(..., description="Display name shown in TWS / Client Portal.")
    rows: Optional[List[WatchlistRow]] = Field(
        None,
        description="Full rows list. If set, conids is ignored.",
    )
    conids: Optional[List[str]] = Field(
        None,
        description="Shortcut: builds rows as [{'C': conid}, ...] when rows is omitted.",
    )

    def ibkr_payload(self) -> Dict[str, Any]:
        if self.rows is not None:
            row_list = [{"C": r.C} for r in self.rows]
        elif self.conids is not None:
            row_list = [{"C": str(c)} for c in self.conids]
        else:
            row_list = []
        return {"id": self.id, "name": self.name, "rows": row_list}


class WatchlistContractsRequest(BaseModel):
    conids: List[str] = Field(..., description="Contract IDs to add to the watchlist.")


def _instruments_to_rows(instruments: Optional[List[dict]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    seen: set[str] = set()
    for inst in instruments or []:
        c = inst.get("C")
        if c is None and inst.get("conid") is not None:
            c = str(inst["conid"])
        if c is None:
            continue
        cs = str(c)
        if cs in seen:
            continue
        seen.add(cs)
        rows.append({"C": cs})
    return rows


async def _fetch_watchlist(client: httpx.AsyncClient, watchlist_id: str) -> dict:
    response = await client.get(
        f"{BASE_URL}/iserver/watchlist",
        params={"id": watchlist_id},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


@router.get(
    "/iserver/watchlists",
    tags=["Watchlists"],
    summary="Get Watchlists",
    description="GET /iserver/watchlists — lists watchlists for the session user. Optional SC=USER_WATCHLIST returns only user-created lists.",
)
async def get_watchlists(
    SC: Optional[str] = Query(
        None,
        description="If USER_WATCHLIST, only user-created watchlists (excludes IB-created).",
    ),
):
    async with httpx.AsyncClient(verify=False) as client:
        try:
            params = {"SC": SC} if SC else None
            response = await client.get(
                f"{BASE_URL}/iserver/watchlists",
                params=params,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            return {
                "error": "IBKR API Error",
                "status_code": exc.response.status_code,
                "detail": exc.response.text,
            }
        except httpx.RequestError as exc:
            return {"error": "Request Error", "detail": str(exc)}


@router.get(
    "/iserver/watchlist",
    tags=["Watchlists"],
    summary="Get Watchlist Contracts",
    description="GET /iserver/watchlist?id= — returns one watchlist including instruments (rows).",
)
async def get_watchlist_contracts(
    id: str = Query(..., description="Watchlist ID."),
):
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(
                f"{BASE_URL}/iserver/watchlist",
                params={"id": id},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            return {
                "error": "IBKR API Error",
                "status_code": exc.response.status_code,
                "detail": exc.response.text,
            }
        except httpx.RequestError as exc:
            return {"error": "Request Error", "detail": str(exc)}


@router.post(
    "/iserver/watchlist",
    tags=["Watchlists"],
    summary="Create Watchlist",
    description="POST /iserver/watchlist with JSON {id, name, rows}. Rows are {'C': conid} objects. Use get_watchlists to pick an unused numeric id.",
)
async def create_watchlist(body: WatchlistCreateRequest = Body(...)):
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.post(
                f"{BASE_URL}/iserver/watchlist",
                json=body.ibkr_payload(),
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            return {
                "error": "IBKR API Error",
                "status_code": exc.response.status_code,
                "detail": exc.response.text,
            }
        except httpx.RequestError as exc:
            return {"error": "Request Error", "detail": str(exc)}


@router.post(
    "/iserver/watchlist/contracts",
    tags=["Watchlists"],
    summary="Add Contracts to Watchlist",
    description="Read-modify-write: GET watchlist, append conids as rows, POST /iserver/watchlist. IBKR exposes no standalone add-contract endpoint.",
)
async def add_contracts_to_watchlist(
    id: str = Query(..., description="Watchlist ID."),
    body: WatchlistContractsRequest = Body(...),
):
    async with httpx.AsyncClient(verify=False) as client:
        try:
            data = await _fetch_watchlist(client, id)
            if data.get("readOnly"):
                return {
                    "error": "Watchlist is read-only",
                    "watchlist_id": id,
                }
            rows = _instruments_to_rows(data.get("instruments"))
            seen = {r["C"] for r in rows}
            for c in body.conids:
                cs = str(c)
                if cs not in seen:
                    seen.add(cs)
                    rows.append({"C": cs})
            payload = {
                "id": str(data["id"]),
                "name": data.get("name") or "",
                "rows": rows,
            }
            response = await client.post(
                f"{BASE_URL}/iserver/watchlist",
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            return {
                "error": "IBKR API Error",
                "status_code": exc.response.status_code,
                "detail": exc.response.text,
            }
        except httpx.RequestError as exc:
            return {"error": "Request Error", "detail": str(exc)}


@router.delete(
    "/iserver/watchlist",
    tags=["Watchlists"],
    summary="Delete Watchlist",
    description="DELETE /iserver/watchlist?id= — removes the watchlist.",
)
async def delete_watchlist(
    id: str = Query(..., description="Watchlist ID to delete."),
):
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.delete(
                f"{BASE_URL}/iserver/watchlist",
                params={"id": id},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            return {
                "error": "IBKR API Error",
                "status_code": exc.response.status_code,
                "detail": exc.response.text,
            }
        except httpx.RequestError as exc:
            return {"error": "Request Error", "detail": str(exc)}


@router.delete(
    "/iserver/watchlist/contracts",
    tags=["Watchlists"],
    summary="Delete Contract from Watchlist",
    description="Read-modify-write: GET watchlist, drop the conid from rows, POST /iserver/watchlist. IBKR exposes no standalone remove-contract endpoint.",
)
async def delete_contract_from_watchlist(
    id: str = Query(..., description="Watchlist ID."),
    conid: str = Query(..., description="Contract ID to remove."),
):
    async with httpx.AsyncClient(verify=False) as client:
        try:
            data = await _fetch_watchlist(client, id)
            if data.get("readOnly"):
                return {
                    "error": "Watchlist is read-only",
                    "watchlist_id": id,
                }
            rows = _instruments_to_rows(data.get("instruments"))
            target = str(conid)
            new_rows = [r for r in rows if r["C"] != target]
            if len(new_rows) == len(rows):
                return {
                    "warning": "Contract was not present on watchlist",
                    "watchlist_id": id,
                    "conid": target,
                    "unchanged": True,
                }
            payload = {
                "id": str(data["id"]),
                "name": data.get("name") or "",
                "rows": new_rows,
            }
            response = await client.post(
                f"{BASE_URL}/iserver/watchlist",
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            return {
                "error": "IBKR API Error",
                "status_code": exc.response.status_code,
                "detail": exc.response.text,
            }
        except httpx.RequestError as exc:
            return {"error": "Request Error", "detail": str(exc)}
