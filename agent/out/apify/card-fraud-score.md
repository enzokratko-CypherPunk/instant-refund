# Card Fraud Score API (Apify / MCP)

## What it does
Fraud risk assessment service

## MCP tool name
card_fraud_scorer

## Inputs
[
  {
    "name": "card_type",
    "type": "string",
    "required": false,
    "example": "prepaid"
  },
  {
    "name": "network",
    "type": "string",
    "required": false,
    "example": "Visa"
  },
  {
    "name": "country_code",
    "type": "string",
    "required": false,
    "example": "US"
  }
]

## Outputs
[
  {
    "name": "fraud_score",
    "type": "number"
  },
  {
    "name": "risk_level",
    "type": "string"
  },
  {
    "name": "recommendation",
    "type": "string"
  }
]

## Example prompt for an AI agent
Score payment card fraud risk using card type, network, and issuing country. Returns fraud_score (0-100), risk_level (low/medium/high), and actionable recommendation for transaction processing.

## Notes
Requires at least one input parameter. Scores are calibrated against industry fraud benchmarks. Use for transaction approval decisions, chargeback prevention, and risk-based pricing.