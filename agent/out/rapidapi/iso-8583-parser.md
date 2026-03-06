# ISO 8583 Parser API

## Title
ISO 8583 Parser API

## Short description
Parse raw ISO 8583 financial transaction messages into structured JSON with field enrichment.

## Long description
ISO 8583 Parser API decodes raw ISO 8583 financial transaction messages from payment networks (Visa, Mastercard, ACH) into human-readable structured JSON. Supports all ISO 8583:1987, :1993, :2003 versions with automatic field interpretation, validation, and merchant/acquirer enrichment. Purpose-built for payment processors, gateway integrators, and fintech platforms managing transaction reconciliation and debugging.

## Keywords / tags
['iso-8583', 'payment-processing', 'iso-decoder', 'financial-messaging', 'transaction-parser', 'payment-gateway', 'fintech', 'banking-api', 'message-format', 'card-networks']

## Example request
curl -X GET 'https://instant-refund-api-l99qr.ondigitalocean.app/v1/tools/iso8583/0100' -H 'Authorization: Bearer YOUR_API_KEY'

## Example response
{"mti":"0100","message_type":"Authorization Request","fields":{"3":{"field_name":"Processing Code","value":"000000","description":"Purchase"},"4":{"field_name":"Amount, Transaction","value":"000000100000","formatted":"$1000.00"},"11":{"field_name":"Systems Trace Audit Number (STAN)","value":"123456"},"12":{"field_name":"Time, Local Transaction","value":"143025"},"13":{"field_name":"Date, Local Transaction","value":"1225"},"35":{"field_name":"Track 2 Data","masked":true},"41":{"field_name":"Card Acceptor Terminal Identification Code","value":"TERM001"}}}

## Pricing copy
Free tier: 100 requests/month. Pro: $29/month (10K requests). Enterprise: Custom volume licensing.