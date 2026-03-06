# Currency Converter API (Apify / MCP)

## What it does
Currency exchange rate lookup and conversion tool

## MCP tool name
currency_converter

## Inputs
[
  {
    "name": "from_currency",
    "type": "string",
    "required": true,
    "example": "USD"
  },
  {
    "name": "to_currency",
    "type": "string",
    "required": true,
    "example": "EUR"
  }
]

## Outputs
[
  {
    "name": "rate",
    "type": "number"
  },
  {
    "name": "converted",
    "type": "number"
  }
]

## Example prompt for an AI agent
Convert currency amounts between any two ISO 4217 currency codes. Provide real-time exchange rates and converted amounts.

## Notes
Supports all ISO 4217 currency codes. Returns current mid-market rates updated every 60 seconds. No rate limiting per request, only monthly quota limits.