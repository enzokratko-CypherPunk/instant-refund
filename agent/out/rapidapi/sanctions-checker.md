# Sanctions Checker API

## Title
Sanctions Checker API

## Short description
Real-time OFAC SDN list screening with fuzzy name matching for compliance and AML workflows.

## Long description
Sanctions Checker API enables instant screening of names and entities against the OFAC Specially Designated Nationals (SDN) list. Built for financial compliance teams, it uses fuzzy matching algorithms to catch variations in spelling, transliteration, and name formatting. Returns match confidence scores and detailed hit information for investigation and audit trails.

## Keywords / tags
['sanctions-screening', 'ofac-compliance', 'aml-kyc', 'fintech', 'regulatory-compliance', 'name-matching', 'risk-management']

## Example request
curl -X GET 'https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/sanctions/John%20Smith' -H 'Authorization: Bearer YOUR_API_KEY'

## Example response
{"match": true, "score": 0.94, "matches": [{"name": "JOHN SMITH", "entity_type": "Individual", "list_source": "OFAC", "confidence": 0.94, "aliases": []}]}

## Pricing copy
Contact sales for volume pricing. Typical: $0.02-0.05 per screening.