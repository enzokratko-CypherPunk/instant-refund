# PEP Screener API

## Title
PEP Screener API

## Short description
Real-time politically exposed persons screening for KYC/AML compliance workflows

## Long description
PEP Screener API enables instant verification of individuals against globally recognized politically exposed persons databases. Essential for financial institutions, fintech platforms, and regulated businesses requiring automated KYC (Know Your Customer) and AML (Anti-Money Laundering) compliance checks. Returns boolean PEP status with risk level classification in milliseconds.

## Keywords / tags
['compliance', 'kyc', 'aml', 'pep-screening', 'fintech', 'identity-verification', 'regulatory', 'risk-assessment']

## Example request
{'method': 'GET', 'url': 'https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/pep/Jane%20Doe', 'headers': {'Accept': 'application/json'}}

## Example response
{'is_pep': False, 'risk_level': 'low'}

## Pricing copy
Contact for enterprise tiers; usage-based models available