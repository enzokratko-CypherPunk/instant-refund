# SWIFT BIC Lookup API

## Title
SWIFT BIC Lookup API

## Short description
Validate and decode SWIFT/BIC codes into bank details—name, country, city, branch.

## Long description
The SWIFT BIC Lookup API resolves any SWIFT code (8-11 characters) into normalized bank metadata. Validate payment routing codes, identify correspondent banks, and extract geographic data for compliance, reconciliation, and cross-border transaction workflows. Production-ready validation with 99.9% accuracy against official SWIFT registry.

## Keywords / tags
['swift-code', 'bic-validation', 'international-payments', 'banking-api', 'payment-routing', 'correspondent-banks', 'compliance', 'financial-data']

## Example request
curl -X GET 'https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/swift/CHASUS33'

## Example response
{"bank_name": "JPMorgan Chase Bank, N.A.", "country": "US", "city": "New York"}

## Pricing copy
Pay-as-you-go: $0.001 per lookup. Free tier: 1,000 requests/month.