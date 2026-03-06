# Decline Code Interpreter API

## Title
Decline Code Interpreter API

## Short description
Translate payment decline codes into actionable insights with plain-English meanings, retry logic, and category classification.

## Long description
The Decline Code Interpreter API instantly converts cryptic payment decline codes (ISO 8583, network-specific, processor-specific) into human-readable explanations, retry guidance, and categorical classification. Eliminate ambiguity in payment failures—understand whether a decline is temporary (retryable) or permanent, and route customer experience accordingly. Support for Visa, Mastercard, Amex, Discover, and ACH decline codes.

## Keywords / tags
['payments', 'decline-codes', 'payment-processing', 'error-handling', 'fintech', 'card-payments', 'api', 'iso-8583']

## Example request
GET https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/decline/51

## Example response
{'code': '51', 'meaning': "Insufficient funds available in customer's account", 'category': 'insufficient_funds', 'retryable': 'false', 'network': 'ISO 8583', 'retry_after': None, 'merchant_action': 'Inform customer to add funds or use different payment method'}

## Pricing copy
Free tier: 100 requests/month. Pro: $29/month (10k requests). Enterprise: custom volume pricing with SLA.