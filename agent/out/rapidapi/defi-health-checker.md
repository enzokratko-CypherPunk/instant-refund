# DeFi Health Checker API

## Title
DeFi Health Checker API

## Short description
Real-time health monitoring for 15 major DeFi protocols with TVL, risk assessment, and 24h metrics.

## Long description
DeFi Health Checker API provides instant protocol health snapshots across Aave, Curve, Lido, MakerDAO, Compound, Uniswap, Yearn, Balancer, Convex, Stargate, GMX, dYdX, Arbitrum, Optimism, and Polygon. Get current TVL in USD, 24-hour change percentages, risk levels (low/medium/high/critical), and health status flags to power risk dashboards, portfolio monitors, and trading bots.

## Keywords / tags
['defi', 'protocol-monitoring', 'tvl-data', 'risk-assessment', 'real-time', 'smart-contracts', 'web3', 'crypto-analytics']

## Example request
curl -X GET 'https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/defi-health/aave' \
  -H 'Authorization: Bearer YOUR_API_KEY'

## Example response
{
  "protocol": "aave",
  "health_status": "healthy",
  "tvl_usd": 8450000000,
  "tvl_24h_change": 2.34,
  "risk_level": "low",
  "timestamp": "2024-01-15T14:32:00Z",
  "collateral_ratio": 1.85,
  "unique_users": 142000
}

## Pricing copy
{'model': 'pay-as-you-go', 'free_tier': '100 requests/month', 'pro': '$29/month - 50,000 requests', 'enterprise': 'Custom - unlimited with SLA'}