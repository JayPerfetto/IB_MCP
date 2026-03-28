# IB MCP — local Docker stack
#
# Client Portal Gateway auth is tied to your machine/browser session, so this
# stack is meant to run locally (not a remote host you SSH into without the
# same login flow). See README "Docker Desktop Setup" for first-time login.
#
# Requires: https://github.com/casey/just — `brew install just`

compose := "docker compose"

# Show recipes (default)
default:
    @just --list

# --- lifecycle ---

# Start stack in background (images must exist; use `up-build` after clone or Dockerfile changes)
up:
    {{compose}} up -d

# Start and rebuild images if needed
up-build:
    {{compose}} up -d --build

# Stop and remove containers
down:
    {{compose}} down

# Restart everything
restart:
    {{compose}} restart

# After editing `mcp_server/routers/*.py` (bind mount; process must reload)
restart-mcp:
    {{compose}} restart mcp_server

restart-gateway:
    {{compose}} restart api_gateway

# --- rebuild images ---

# Rebuild all images without cache, then start
rebuild-fresh:
    {{compose}} down
    {{compose}} build --no-cache
    {{compose}} up -d

# Rebuild and recreate all services (uses cache)
rebuild:
    {{compose}} up -d --build

rebuild-mcp:
    {{compose}} up -d --build mcp_server

rebuild-gateway:
    {{compose}} up -d --build api_gateway

# --- observe ---

ps:
    {{compose}} ps

logs *args:
    {{compose}} logs -f {{args}}

logs-mcp:
    {{compose}} logs -f mcp_server

logs-gateway:
    {{compose}} logs -f api_gateway
