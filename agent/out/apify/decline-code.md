# Decline Code Interpreter API (Apify / MCP)

## What it does
API that decodes payment decline codes and returns actionable merchant guidance

## MCP tool name
decline_code_interpreter

## Inputs
[
  {
    "name": "code",
    "type": "string",
    "required": true,
    "example": "51"
  }
]

## Outputs
[
  {
    "name": "meaning",
    "type": "string"
  },
  {
    "name": "retryable",
    "type": "string"
  },
  {
    "name": "category",
    "type": "string"
  }
]

## Example prompt for an AI agent
You are a payment decline code expert. When given a decline code, provide the exact meaning, whether it's retryable, and the merchant action required. Reference ISO 8583 standards and card network specifications.

## Notes
Supports ISO 8583, Visa VRF, Mastercard, Amex, Discover, ACH, and processor-specific codes. Returns retry guidance and customer-facing messaging templates.