# MCC Lookup API

## Title
MCC Lookup API

## Short description
Decode 4-digit Merchant Category Codes into standardized categories and descriptions for payment processing, risk assessment, and transaction classification.

## Long description
The MCC Lookup API instantly resolves any 4-digit Merchant Category Code (MCC) to its official category name and detailed description. Essential for payment processors, fintech platforms, and compliance systems that need to classify merchants, validate transaction categories, or implement category-based rules and restrictions. Supports all ISO 18245 merchant category codes with instant lookups and zero external dependencies.

## Keywords / tags
['payments', 'mcc', 'merchant-classification', 'compliance', 'transaction-processing', 'payment-processing', 'fintech', 'iso-18245', 'category-codes']

## Example request
curl -X GET 'https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/mcc/5411'

## Example response
{"category": "Groceries", "description": "Supermarkets, self-service stores, and grocery retailers"}

## Pricing copy
Contact sales for volume pricing. Free tier: 100 requests/day. Pro: $29/mo (10k req/day). Enterprise: Custom rates.