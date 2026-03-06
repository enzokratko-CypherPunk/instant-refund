# Payment Intelligence API

## Title
Payment Intelligence API

## Short description
Analyze payment failures with decline codes, BIN data, and fraud scoring. Get actionable retry strategies and risk assessments in real-time.

## Long description
Payment Intelligence API provides full-spectrum analysis of payment transactions. Input BIN, decline code, MCC, and amount to receive retry probability scoring, fraud risk assessment, and plain-English recommendations for payment recovery. Optimize retry logic, reduce false declines, and improve payment success rates.

## Keywords / tags
['payments', 'decline-analysis', 'fraud-detection', 'retry-strategy', 'payment-optimization', 'fintech', 'transaction-intelligence']

## Example request
{'method': 'GET', 'url': 'https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/payment-intelligence?card_bin=411111&decline_code=51&merchant_mcc=5411&transaction_amount=250.0', 'headers': {'Content-Type': 'application/json'}}

## Example response
{'recommendation': 'Retry with 3D Secure authentication after 2 minutes', 'retry_probability_pct': 73.5, 'fraud_score': 12}

## Pricing copy
{'model': 'pay-as-you-go', 'free_tier': True, 'per_request_usd': 0.001}