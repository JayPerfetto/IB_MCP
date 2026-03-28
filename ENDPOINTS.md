# IB API Endpoints (Total: 79)

## Alerts (5)

| Method | Endpoint                                     | Description                                          | Status |
|--------|----------------------------------------------|------------------------------------------------------|--------|
| `POST` | `/iserver/account/alert/activate`            | Activates or deactivates an existing alert.          | 🟠     |
| `GET`  | `/iserver/account/mta`                       | Retrieves the Mobile Trading Assistant (MTA) alert.  | 🟠     |
| `POST` | `/iserver/account/{accountId}/alert`         | Creates a new alert or modifies an existing one.     | 🟠     |
| `DELETE` | `/iserver/account/{accountId}/alert/{alertId}` | Deletes a single alert for the given account.        | 🟠     |
| `GET`  | `/iserver/account/{accountId}/alerts`        | Returns a list of alerts for the specified account.  | 🟠     |

## Contract (13)

| Method | Endpoint                                   | Description                                                     | Status |
|--------|--------------------------------------------|-----------------------------------------------------------------|--------|
| `GET`  | `/iserver/contract/{conid}/algos`          | Returns a list of available IB Algos for a contract.            | 🟠     |
| `GET`  | `/iserver/contract/{conid}/info`           | Get full contract details for a given contract ID (conid).      | 🟠     |
| `GET`  | `/iserver/contract/{conid}/info-and-rules` | Returns a conglomeration of contract information and trading rules. | 🟠     |
| `POST` | `/iserver/contract/rules`                  | Returns trading rules for a contract.                           | 🟠     |
| `GET`  | `/iserver/secdef/bond-filters`             | Returns a list of available bond filters for a given issuer.    | 🟢     |
| `GET`  | `/iserver/secdef/currency`                 | Search for currency pairs.                                      | 🟠     |
| `GET`  | `/iserver/secdef/info`                     | Provides security definition and rules information for a given conid. | 🟠     |
| `GET`  | `/iserver/secdef/search`                   | Search for contracts by symbol or company name.                 | 🟢     |
| `GET`  | `/iserver/secdef/strikes`                  | Get a list of available option strikes for a given underlying.  | 🟠     |
| `GET`  | `/trsrv/futures`                           | Returns a list of futures for the given symbols.                | 🟠     |
| `GET`  | `/trsrv/secdef`                            | Returns a list of security definitions for the given conids.    | 🟠     |
| `GET`  | `/trsrv/secdef/schedule`                   | Returns the trading schedule for a contract.                    | 🟠     |
| `GET`  | `/trsrv/stocks`                            | Returns a list of stock contracts for the given symbols.        | 🟠     |

## Events Contracts (2)

| Method | Endpoint            | Description                                         | Status |
|--------|---------------------|-----------------------------------------------------|--------|
| `GET`  | `/events/contracts` | Returns a list of event contracts for given conids. | 🟠     |
| `GET`  | `/events/show`      | Returns the event contract for a given conid.       | 🟠     |

## FA Allocation Management (2)

| Method | Endpoint     | Description                                 | Status |
|--------|--------------|---------------------------------------------|--------|
| `POST` | `/fa/groups` | Creates a new FA allocation group.          | 🟠     |
| `GET`  | `/fa/groups` | Returns a list of all FA allocation groups. | 🟠     |

## FYIs and Notifications (8)

| Method | Endpoint                      | Description                                          | Status |
|--------|-------------------------------|------------------------------------------------------|--------|
| `POST` | `/fyi/deliveryoptions`        | Enables or disables a delivery option.               | 🟠     |
| `GET`  | `/fyi/deliveryoptions`        | Returns a list of all supported delivery options.    | 🟠     |
| `PUT`  | `/fyi/deliveryoptions/device` | Enables or disables notifications for a device.      | 🟠     |
| `DELETE` | `/fyi/notifications`          | Marks a list of notifications as read.               | 🟠     |
| `GET`  | `/fyi/notifications`          | Returns a list of notifications.                     | 🟠     |
| `POST` | `/fyi/settings`               | Returns a list of disclaimer-type notifications.     | 🟠     |
| `PUT`  | `/fyi/settings/{typecode}`    | Enables or disables a specific disclaimer type.      | 🟠     |
| `GET`  | `/fyi/unreadnumber`           | Returns the total number of unread FYI notifications.| 🟠     |

## Market Data (10)

| Method | Endpoint                               | Description                                                     | Status |
|--------|----------------------------------------|-----------------------------------------------------------------|--------|
| `GET`  | `/hmds/history`                        | Get historical market data from the HMDS.                       | 🟠     |
| `GET`  | `/iserver/marketdata/availability`     | Returns a dictionary explaining market data availability codes. | 🟠     |
| `GET`  | `/iserver/marketdata/bars`             | Returns a dictionary of valid bar units for historical data.    | 🟠     |
| `GET`  | `/iserver/marketdata/fields`           | Returns a list of all available fields for snapshots.           | 🟠     |
| `GET`  | `/iserver/marketdata/history`          | Get historical market data for a contract.                      | 🟢     |
| `GET`  | `/iserver/marketdata/periods`          | Returns a dictionary of valid period units for historical data. | 🟠     |
| `GET`  | `/iserver/marketdata/snapshot`         | Get a snapshot of market data for one or more contracts.        | 🟢     |
| `POST` | `/iserver/marketdata/unsubscribe`      | Unsubscribes from a specific market data feed.                  | 🟠     |
| `POST` | `/iserver/marketdata/unsubscribeall`   | Unsubscribes from all current market data subscriptions.        | 🟠     |
| `GET`  | `/md/snapshot`                         | Get a non-streaming snapshot of market data for conids.         | 🟠     |

## Options Chains (1)

| Method | Endpoint               | Description                                | Status |
|--------|------------------------|--------------------------------------------|--------|
| `GET`  | `/trsrv/secdef/chains` | Returns the option chain for a given symbol. | 🟠     |

## Order Monitoring (3)

| Method | Endpoint                                | Description                                                     | Status |
|--------|-----------------------------------------|-----------------------------------------------------------------|--------|
| `GET`  | `/iserver/account/order/status/{orderId}` | Retrieves the status of a single order by its order ID.         | 🟠     |
| `GET`  | `/iserver/account/orders`               | Retrieves a list of live orders.                                | 🟠     |
| `GET`  | `/iserver/account/trades`               | Returns a list of trades for the current and previous six days. | 🟠     |

## Orders (5)

| Method | Endpoint                                     | Description                                                        | Status |
|--------|----------------------------------------------|--------------------------------------------------------------------|--------|
| `DELETE` | `/iserver/account/{accountId}/order/{orderId}` | Cancels an open order.                                             | 🟠     |
| `POST` | `/iserver/account/{accountId}/order/{orderId}` | Modifies an existing open order.                                   | 🟠     |
| `POST` | `/iserver/account/{accountId}/orders`        | Places one or more orders.                                         | 🟠     |
| `POST` | `/iserver/account/{accountId}/orders/whatif` | Previews an order without submitting it.                           | 🟠     |
| `POST` | `/iserver/reply/{replyId}`                   | Replies to a confirmation message for an order.                    | 🟠     |

## Portfolio (13)

| Method | Endpoint                                      | Description                                                                                                                    | Status          |
|--------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|-----------------|
| `GET`  | `/portfolio/accounts`                         | Returns a list of accounts for viewing position and account information.                                                      | 🟢         |
| `POST` | `/portfolio/allocation`                       | Returns allocation information for multiple accounts combined.                                                                 | 🟠   |
| `GET`  | `/portfolio/positions/{conid}`                | Returns all positions for a contract ID across all accounts, along with contract info.                                         | 🟢   |
| `GET`  | `/portfolio/subaccounts`                      | Returns up to 100 sub-accounts for viewing position and account information in tiered structures.                             | 🟢  |
| `GET`  | `/portfolio/subaccounts2`                     | Returns sub-accounts for large tiered account structures.                                                                      | 🟠   |
| `GET`  | `/portfolio/{accountId}/allocation`           | Returns position allocation by asset class, industry, and category for a single account.                                       | 🟠       |
| `GET`  | `/portfolio/{accountId}/combo/positions`      | Returns combination positions (e.g., complex options) for a single account.                                                    | 🟠       |
| `GET`  | `/portfolio/{accountId}/ledger`               | Returns the cash balance and ledger information for a specific account.                                                        | 🟠  |
| `GET`  | `/portfolio/{accountId}/meta`                 | Returns metadata (name, currency, etc.) for a specific account.                                                                | 🟠     |
| `POST` | `/portfolio/{accountId}/positions/invalidate` | Invalidates backend cache for the account's portfolio data.                                                                    | 🟠  |
| `GET`  | `/portfolio/{accountId}/positions/{pageId}`   | Returns paginated positions for a specific account.                                                                            | 🟠  |
| `GET`  | `/portfolio/{accountId}/summary`              | Returns a summary of account information and portfolio positions.                                                              | 🟢|
| `GET`  | `/portfolio/{acctId}/position/{conid}`        | Returns all positions for a given contract ID within a specific account.                                                       | 🟢    |

## Portfolio Analyst (3)

| Method | Endpoint          | Description                                                  | Status |
|--------|-------------------|--------------------------------------------------------------|--------|
| `POST` | `/pa/allperiods`  | Returns a list of all available periods for PA data.         | 🟠     |
| `POST` | `/pa/performance` | Returns the performance (NAV) of specified account(s).       | 🟠     |
| `POST` | `/pa/transactions`| Returns a list of transactions for specified account(s).     | 🟠     |

## Scanner (3)

| Method | Endpoint                  | Description                                                  | Status |
|--------|---------------------------|--------------------------------------------------------------|--------|
| `POST` | `/hmds/scanner`           | Runs a scanner on the Historical Market Data Service.        | 🟠     |
| `GET`  | `/iserver/scanner/params` | Returns an XML file with available iServer scanner parameters. | 🟠     |
| `POST` | `/iserver/scanner/run`    | Runs an iServer market scanner search.                       | 🟠     |

## Session (5)

| Method | Endpoint                  | Description                                                       | Status |
|--------|---------------------------|-------------------------------------------------------------------|--------|
| `GET`  | `/iserver/auth/status`    | Returns the authentication status of the gateway.                 | 🟠     |
| `POST` | `/iserver/reauthenticate` | Attempts to re-authenticate an expired session.                   | 🟠     |
| `POST` | `/logout`                 | Logs the user out of the gateway session.                         | 🟠     |
| `POST` | `/sso/validate`           | Validates the current session for the SSO user.                   | 🟠     |
| `GET`  | `/tickle`                 | Keeps the session open and verifies gateway is running.           | 🟠     |

## Watchlists (6)

These MCP routes proxy the [IB REST API](https://www.interactivebrokers.com/campus/ibkr-api-page/webapi-ref/) watchlist endpoints (`/iserver/watchlists`, `/iserver/watchlist`). The last two rows are **composite** helpers: IBKR has no standalone add/remove-contract calls; they GET the list, change `rows`, then `POST` the full watchlist.

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| `GET` | `/iserver/watchlists` | Lists watchlists. Optional query `SC=USER_WATCHLIST` (user-created only). Proxies `GET /iserver/watchlists`. | 🟠 |
| `GET` | `/iserver/watchlist` | Single watchlist with instruments. Query `id=<watchlistId>`. Proxies `GET /iserver/watchlist?id=`. | 🟠 |
| `POST` | `/iserver/watchlist` | Create/replace watchlist. JSON body: `id` (numeric string), `name`, `rows` as `[{"C":"<conid>"}, ...]` or shortcut field `conids`. Proxies `POST /iserver/watchlist`. | 🟠 |
| `DELETE` | `/iserver/watchlist` | Delete watchlist. Query `id=<watchlistId>`. Proxies `DELETE /iserver/watchlist?id=`. | 🟠 |
| `POST` | `/iserver/watchlist/contracts` | Add contracts: query `id`, body `{"conids":["..."]}`. Read-modify-write via `GET` + `POST /iserver/watchlist`. | 🟠 |
| `DELETE` | `/iserver/watchlist/contracts` | Remove one contract: query `id` and `conid`. Read-modify-write via `GET` + `POST /iserver/watchlist`. | 🟠 |


## Status categories

| Icon | Status           |
|------|------------------|
| 🟢   | Ready            |
| 🟡   | Work in Progress |
| 🔘   | Not started      |
| 🟠   | Not tested       |
