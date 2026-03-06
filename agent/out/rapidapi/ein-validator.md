# EIN Validator API

## Title
EIN Validator API

## Short description
Validate US Employer Identification Numbers against IRS prefix rules in real-time.

## Long description
The EIN Validator API checks whether a provided Employer Identification Number (EIN) conforms to IRS assignment logic and prefix validation rules. Returns validity status, issuing campus location, and prefix information for compliance verification and business identity validation workflows.

## Keywords / tags
['compliance', 'validation', 'business-identity', 'tax-id', 'irs', 'ein-lookup', 'regulatory']

## Example request
GET https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/ein/26-0000618

## Example response
{'valid': True, 'issuing_campus': 'Philadelphia', 'prefix': '26'}

## Pricing copy
Contact sales for custom volume pricing