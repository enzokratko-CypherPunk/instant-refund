# BIN Lookup API

## Title
BIN Lookup API

## Short description
Identify card issuer, network, type, and country from BIN code in milliseconds.

## Long description
Real-time BIN (Bank Identification Number) lookup API for payment processing. Extract issuer bank name, card network (Visa, Mastercard, etc.), card type (credit, debit, prepaid), and issuing country from the first 6-8 digits. Essential for payment fraud prevention, card validation, and financial risk assessment workflows.

## Keywords / tags
['payments', 'bin-lookup', 'card-validation', 'fraud-detection', 'payment-processing', 'fintech', 'issuer-identification', 'card-metadata']

## Example request
{'method': 'GET', 'url': 'https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/bin/411111', 'headers': {'Content-Type': 'application/json'}}

## Example response
{'bin_code': '411111', 'bank': 'Chase Bank', 'network': 'Visa', 'card_type': 'credit', 'country': 'US'}

## Pricing copy
{'model': 'pay-as-you-go', 'free_tier': '100 requests/month', 'typical_cost': '$0.001 per lookup'}