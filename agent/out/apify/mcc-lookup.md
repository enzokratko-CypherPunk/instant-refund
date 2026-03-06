# MCC Lookup API (Apify / MCP)

## What it does
API that translates ISO 18245 Merchant Category Codes into human-readable classifications

## MCP tool name
mcc_lookup_tool

## Inputs
[
  {
    "name": "mcc_code",
    "type": "string",
    "required": true,
    "example": "5411"
  }
]

## Outputs
[
  {
    "name": "description",
    "type": "string"
  },
  {
    "name": "category",
    "type": "string"
  }
]

## Example prompt for an AI agent
You are an MCC lookup assistant. When given a 4-digit merchant category code, return the standardized category name and business description. Use the MCC Lookup API endpoint at /v1/tools/mcc/{mcc_code} to resolve codes instantly.

## Notes
Returns both category and description fields. Supports all valid ISO 18245 MCCs (1000-9999 range). Useful for real-time merchant classification in payment workflows.