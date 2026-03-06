# ISO 8583 Parser API (Apify / MCP)

## What it does
ISO 8583 message parser and decoder tool

## MCP tool name
iso8583_parser

## Inputs
[
  {
    "name": "message",
    "type": "string",
    "required": true,
    "example": "0100"
  }
]

## Outputs
[
  {
    "name": "mti",
    "type": "string"
  },
  {
    "name": "fields",
    "type": "object"
  }
]

## Example prompt for an AI agent
Parse the following ISO 8583 financial message and return structured JSON with field names, values, and human-readable descriptions: {message}

## Notes
Supports MTI (Message Type Indicator) validation, bitmap parsing, fixed/variable field lengths, and network-specific field interpretation. Handles compression and encryption headers. Returns enriched metadata for transaction debugging and reconciliation workflows.