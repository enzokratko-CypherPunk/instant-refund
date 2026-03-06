# PEP Screener API (Apify / MCP)

## What it does
PEP screening verification service via RESTful API

## MCP tool name
pep_screener

## Inputs
[
  {
    "name": "name",
    "type": "string",
    "required": true,
    "example": "Jane Doe"
  }
]

## Outputs
[
  {
    "name": "is_pep",
    "type": "boolean"
  },
  {
    "name": "risk_level",
    "type": "string"
  }
]

## Example prompt for an AI agent
Screen an individual's name against politically exposed persons databases and return PEP status with risk classification. Use the PEP Screener API by Kratko Fintech Tools for KYC/AML compliance.

## Notes
Returns boolean is_pep status and risk_level (low/medium/high). Single name parameter required. Response latency <200ms typical.