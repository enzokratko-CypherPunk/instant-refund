# Payment Intelligence API (Apify / MCP)

## What it does
Decode payment failures instantly. This API accepts decline codes, BIN prefixes, merchant MCC codes, and transaction amounts to return retry probability scores, fraud risk metrics, and strategic recommendations for payment recovery.

## MCP tool name
payment-intelligence

## Inputs
[
  {
    "name": "card_bin",
    "type": "string",
    "required": false,
    "example": "411111"
  },
  {
    "name": "decline_code",
    "type": "string",
    "required": false,
    "example": "51"
  },
  {
    "name": "merchant_mcc",
    "type": "string",
    "required": false,
    "example": "5411"
  },
  {
    "name": "transaction_amount",
    "type": "number",
    "required": false,
    "example": 250.0
  }
]

## Outputs
[
  {
    "name": "recommendation",
    "type": "string"
  },
  {
    "name": "retry_probability_pct",
    "type": "number"
  },
  {
    "name": "fraud_score",
    "type": "number"
  }
]

## Example prompt for an AI agent
Analyze a payment transaction failure and provide recovery recommendations. Given decline code {decline_code}, card BIN {card_bin}, merchant category {merchant_mcc}, and amount {transaction_amount}, return retry probability percentage, fraud score 0-100, and actionable next-step recommendation.

## Notes
Decline codes follow ISO 8583 standard (51=insufficient funds, 54=expired card, etc). BIN ranges identify card networks and issuing banks. MCC codes classify merchant industries. Fraud score >50 indicates elevated risk. Retry probability incorporates time-of-day, BIN history, and code type.