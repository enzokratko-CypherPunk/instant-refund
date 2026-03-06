# Routing Number Validator API (Apify / MCP)

## What it does
Validates US ABA routing numbers against Federal Reserve database, returns bank issuer and district.

## MCP tool name
routing_number_validator

## Inputs
[
  {
    "name": "routing_number",
    "type": "string",
    "required": true,
    "example": "021000021"
  }
]

## Outputs
[
  {
    "name": "valid",
    "type": "boolean"
  },
  {
    "name": "bank_name",
    "type": "string"
  },
  {
    "name": "fed_district",
    "type": "string"
  }
]

## Example prompt for an AI agent
Validate a US routing number and retrieve the issuing bank name and Federal Reserve district assignment using the Routing Number Validator API.

## Notes
Input must be exactly 9 digits. Returns structured JSON. No authentication required for basic tier.