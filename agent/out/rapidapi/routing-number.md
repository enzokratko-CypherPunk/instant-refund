# Routing Number Validator API

## Title
Routing Number Validator API

## Short description
Validate US ABA routing numbers and identify issuing banks and Federal Reserve districts in real-time.

## Long description
The Routing Number Validator API provides instant validation of 9-digit ABA routing numbers used in US domestic banking. Returns bank identification, Federal Reserve district assignment, and validity status. Essential for payment processing, ACH transfers, wire setup, and financial compliance workflows.

## Keywords / tags
['routing-number-validation', 'aba-lookup', 'bank-identification', 'payment-infrastructure', 'fintech-compliance', 'fed-district', 'ach-processing']

## Example request
GET https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/routing/021000021

## Example response
{'valid': True, 'bank_name': 'Federal Reserve Bank of New York', 'fed_district': '2'}

## Pricing copy
Per-request billing. First 1,000 requests/month free tier. $0.001 per additional request.