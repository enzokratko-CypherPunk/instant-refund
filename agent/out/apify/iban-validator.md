# IBAN Validator API (Apify / MCP)

## What it does
IBAN checksum validation and component parsing tool

## MCP tool name
iban-validator

## Inputs
[
  {
    "name": "iban_code",
    "type": "string",
    "required": true,
    "example": "GB82WEST12345698765432"
  }
]

## Outputs
[
  {
    "name": "valid",
    "type": "boolean"
  },
  {
    "name": "country",
    "type": "string"
  },
  {
    "name": "bank_code",
    "type": "string"
  }
]

## Example prompt for an AI agent
Validate IBAN account numbers and extract banking details. Use this tool to verify international bank account numbers before processing payments, ensuring compliance with SEPA standards and preventing invalid transfers.

## Notes
Returns boolean validity status plus extracted country code and bank code. Supports all ISO 13616 compliant IBAN formats. Ideal for payment gateway validation, KYC workflows, and cross-border transaction screening.