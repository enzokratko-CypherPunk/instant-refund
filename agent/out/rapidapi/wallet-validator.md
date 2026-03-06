# Crypto Wallet Address Validator API

## Title
Crypto Wallet Address Validator API

## Short description
Validate crypto wallet addresses across 20+ blockchains in real-time

## Long description
Multi-chain wallet address validator supporting Bitcoin, Ethereum, Solana, Kaspa, and 16+ additional blockchain networks. Returns validation status, detected chain, and network information with sub-millisecond response times.

## Keywords / tags
['crypto', 'wallet', 'blockchain', 'validation', 'bitcoin', 'ethereum', 'solana', 'address-verification']

## Example request
curl -X GET 'https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/wallet/0x742d35Cc6634C0532925a3b844Bc454e4438f44e' -H 'Authorization: Bearer YOUR_API_KEY'

## Example response
{'valid': True, 'chain': 'ethereum', 'network': 'mainnet'}

## Pricing copy
Pay-as-you-go: $0.001 per validation request. Free tier: 100 requests/month.