# DeFi Health Checker API (Apify / MCP)

## What it does
Monitors on-chain DeFi protocol metrics including total value locked, user activity, collateral ratios, and risk indicators via smart contract state queries and subgraph indexing.

## MCP tool name
defi_health_checker

## Inputs
[
  {
    "name": "protocol",
    "type": "string",
    "required": true,
    "example": "aave"
  }
]

## Outputs
[
  {
    "name": "health_status",
    "type": "string"
  },
  {
    "name": "tvl_usd",
    "type": "number"
  },
  {
    "name": "risk_level",
    "type": "string"
  }
]

## Example prompt for an AI agent
Check the health status and TVL of [protocol] including risk level, 24h change, and user metrics

## Notes
Supports: aave, curve, lido, makerdao, compound, uniswap, yearn, balancer, convex, stargate, gmx, dydx, arbitrum, optimism, polygon. Rate limits: 100 req/sec. Cache: 60s TTL.