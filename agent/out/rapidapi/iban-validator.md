# IBAN Validator API

## Title
IBAN Validator API

## Short description
Validate IBAN checksums and parse bank/country/account components in real-time.

## Long description
IBAN Validator API provides instant validation of International Bank Account Numbers (IBANs) with checksum verification and component extraction. Extract country codes, bank identifiers, and account numbers from any IBAN string. Supports all SEPA and international IBAN formats.

## Keywords / tags
['iban-validation', 'payments', 'banking', 'sepa', 'international-transfers', 'compliance', 'fintech']

## Example request
{'method': 'GET', 'url': 'https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/iban/GB82WEST12345698765432', 'headers': {'Content-Type': 'application/json'}}

## Example response
{'valid': True, 'country': 'GB', 'bank_code': 'WEST', 'account': '12345698765432', 'status_code': 200}

## Pricing copy
{'model': 'pay-as-you-go', 'free_tier': '100 validations/month', 'standard': '$0.001 per validation', 'volume_discounts': True}