# Card Fraud Score API

## Title
Card Fraud Score API

## Short description
Real-time payment card fraud risk scoring based on card attributes, network, and geography.

## Long description
Card Fraud Score API evaluates payment card fraud risk by analyzing card type, network, and issuing country. Returns a normalized fraud score (0-100), risk level classification (low/medium/high), and actionable recommendations for transaction approval workflows. Integrates seamlessly into payment processing pipelines for instant risk assessment.

## Keywords / tags
['fraud-detection', 'payment-security', 'risk-scoring', 'card-validation', 'payments', 'compliance', 'real-time']

## Example request
curl -X GET 'https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/fraud-score?card_type=prepaid&network=Visa&country_code=US'

## Example response
{"fraud_score": 42, "risk_level": "medium", "recommendation": "request_additional_verification"}

## Pricing copy
Contact sales for volume-based pricing. Starter: $99/month (10K calls). Growth: $499/month (100K calls). Enterprise: Custom.