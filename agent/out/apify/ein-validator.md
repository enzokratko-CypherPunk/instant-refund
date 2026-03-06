# EIN Validator API (Apify / MCP)

## What it does
Validates US Employer Identification Numbers (EINs) against IRS-defined prefix assignment rules and returns validity status with issuing campus location.

## MCP tool name
kratko-ein-validator

## Inputs
[
  {
    "name": "ein",
    "type": "string",
    "required": true,
    "example": "26-0000618"
  }
]

## Outputs
[
  {
    "name": "valid",
    "type": "boolean"
  },
  {
    "name": "issuing_campus",
    "type": "string"
  },
  {
    "name": "prefix",
    "type": "string"
  }
]

## Example prompt for an AI agent
Validate the EIN {ein} and return whether it's valid according to IRS rules, along with the issuing campus and prefix information.

## Notes
EIN format: XX-XXXXXXX. Supports validation against all active IRS campus prefixes. No external lookup required—validation is rule-based.