# BIN Lookup API (Apify / MCP)

## What it does
BIN Lookup API identifies payment card issuer, network, type, and country from Bank Identification Number codes for real-time card validation and fraud prevention.

## MCP tool name
bin_lookup_tool

## Inputs
[
  {
    "name": "bin_code",
    "type": "string",
    "required": true,
    "example": "411111"
  }
]

## Outputs
[
  {
    "name": "bank",
    "type": "string"
  },
  {
    "name": "network",
    "type": "string"
  },
  {
    "name": "card_type",
    "type": "string"
  },
  {
    "name": "country",
    "type": "string"
  }
]

## Example prompt for an AI agent
Use this tool to instantly identify card issuer bank, payment network (Visa/Mastercard/Amex), card type (credit/debit/prepaid), and country of origin from a 6-8 digit BIN code. Required parameter: bin_code (string). Returns bank name, network, card_type, and country.

## Notes
Fast sub-50ms response times. Supports BIN codes 6-8 digits. Global coverage for Visa, Mastercard, American Express, Discover, and regional networks. Ideal for payment gateways, fraud detection systems, and card validation workflows.