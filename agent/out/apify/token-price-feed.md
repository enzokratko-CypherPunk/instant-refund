# Token Price Feed API (Apify / MCP)

## What it does
Real-time cryptocurrency price data API endpoint returning current token price, 24-hour percentage change, and market capitalization for 25+ supported tokens.

## MCP tool name
token_price_feed

## Inputs
[
  {
    "name": "token",
    "type": "string",
    "required": true,
    "example": "btc"
  },
  {
    "name": "currency",
    "type": "string",
    "required": false,
    "example": "usd"
  }
]

## Outputs
[
  {
    "name": "price",
    "type": "number"
  },
  {
    "name": "price_change_24h_pct",
    "type": "number"
  },
  {
    "name": "market_cap",
    "type": "number"
  }
]

## Example prompt for an AI agent
Fetch current price and market data for a cryptocurrency token. Provide token symbol (e.g., 'btc', 'eth') and optional currency code (default: 'usd'). Returns price in specified currency, 24-hour percentage change, and market cap.

## Notes
Supports tokens: BTC, ETH, XRP, ADA, SOL, DOT, LINK, MATIC, AVAX, FTM, ARB, OP, BLAST, etc. Currency parameter accepts ISO 4217 codes (usd, eur, gbp, jpy). Responses cached for 60 seconds.