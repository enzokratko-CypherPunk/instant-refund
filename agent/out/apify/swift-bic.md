# SWIFT BIC Lookup API (Apify / MCP)

## What it does
Instant SWIFT/BIC code validation and bank metadata extraction for international payments and compliance workflows.

## MCP tool name
swift_bic_lookup

## Inputs
[
  {
    "name": "swift_code",
    "type": "string",
    "required": true,
    "example": "CHASUS33"
  }
]

## Outputs
[
  {
    "name": "bank_name",
    "type": "string"
  },
  {
    "name": "country",
    "type": "string"
  },
  {
    "name": "city",
    "type": "string"
  }
]

## Example prompt for an AI agent
Decode SWIFT/BIC codes into bank names, countries, and cities. Example: CHASUS33 → JPMorgan Chase Bank, US, New York.

## Notes
8-11 character alphanumeric codes only. Returns structured bank details for payment routing and KYB verification.