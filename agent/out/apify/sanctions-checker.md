# Sanctions Checker API (Apify / MCP)

## What it does
OFAC sanctions screening tool using fuzzy name matching

## MCP tool name
sanctions-checker

## Inputs
[
  {
    "name": "name",
    "type": "string",
    "required": true,
    "example": "John Smith"
  }
]

## Outputs
[
  {
    "name": "match",
    "type": "boolean"
  },
  {
    "name": "score",
    "type": "number"
  },
  {
    "name": "matches",
    "type": "array"
  }
]

## Example prompt for an AI agent
Screen a name or entity against OFAC SDN sanctions list and return match confidence score.

## Notes
Handles transliteration variations, partial matches, and returns confidence scoring for compliance teams.