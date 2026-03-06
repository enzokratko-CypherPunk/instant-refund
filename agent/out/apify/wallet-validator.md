# Crypto Wallet Address Validator API (Apify / MCP)

## What it does
API endpoint that validates cryptocurrency wallet addresses across multiple blockchain networks and returns chain identification with validation status.

## MCP tool name
wallet_validator

## Inputs
[
  {
    "name": "address",
    "type": "string",
    "required": true,
    "example": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
  }
]

## Outputs
[
  {
    "name": "valid",
    "type": "boolean"
  },
  {
    "name": "chain",
    "type": "string"
  },
  {
    "name": "network",
    "type": "string"
  }
]

## Example prompt for an AI agent
Validate a cryptocurrency wallet address and determine which blockchain network it belongs to using the Crypto Wallet Address Validator API.

## Notes
Supports address formats: P2PKH, P2SH, Bech32 (Bitcoin); ERC-20 standard (Ethereum); Base58 (Solana); Kaspa addresses. Returns chain name and network type (mainnet/testnet).