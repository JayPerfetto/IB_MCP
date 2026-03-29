import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, MCPType

from mcp_server.config import (
    EXCLUDED_TAGS_SET,
    FINAL_DESCRIPTION,
    MCP_SERVER_HOST,
    MCP_SERVER_PORT,
    MCP_TRANSPORT_PROTOCOL,
    SESSION_WATCHDOG_ENABLED,
)
from mcp_server.session_watchdog import session_watchdog_loop

# Import Router Files
import alerts
import contract
import events_contracts
import fa_allocation_management
import fyis_and_notifications
import market_data
import options_chains
import order_monitoring
import orders
import portfolio
import scanner
import session
import watchlists


def _short_openapi_operation_id(route: APIRoute) -> str:
    """Use handler name as operationId so MCP tool names stay short (Cursor caps server+tool at 60 chars)."""
    return route.name


@asynccontextmanager
async def _app_lifespan(app: FastAPI):
    watchdog_task: asyncio.Task[None] | None = None
    if SESSION_WATCHDOG_ENABLED:
        watchdog_task = asyncio.create_task(
            session_watchdog_loop(),
            name="ibkr_session_watchdog",
        )
    yield
    if watchdog_task is not None:
        watchdog_task.cancel()
        try:
            await watchdog_task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="IBKR API",
    description=FINAL_DESCRIPTION,
    version="1.0.0",
    generate_unique_id_function=_short_openapi_operation_id,
    lifespan=_app_lifespan,
)

app.include_router(alerts.router)
app.include_router(contract.router)
app.include_router(events_contracts.router)
app.include_router(fa_allocation_management.router)
app.include_router(fyis_and_notifications.router)
app.include_router(market_data.router)
app.include_router(options_chains.router)
app.include_router(order_monitoring.router)
app.include_router(orders.router)
app.include_router(portfolio.router)
app.include_router(scanner.router)
app.include_router(session.router)
app.include_router(watchlists.router)


route_maps_list = []

if EXCLUDED_TAGS_SET:    
    for tag_ in EXCLUDED_TAGS_SET:
        route_maps_list.append(RouteMap(tags={tag_}, mcp_type=MCPType.EXCLUDE))


mcp = FastMCP.from_fastapi(
    app=app,
    route_maps = route_maps_list,
    )

if __name__ == "__main__":
    mcp.run(
        transport=MCP_TRANSPORT_PROTOCOL,
        host=MCP_SERVER_HOST,
        port=MCP_SERVER_PORT,
        log_level="DEBUG",
    )
