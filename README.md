# Settlement Assurance Engine — Instant Refund API

A production-grade FastAPI service that delivers cryptographic settlement finality for payment refunds using the Kaspa blockchain as an immutable confirmation layer.

## What It Does

When a refund is initiated, the system captures the transaction ID and anchors it to the Kaspa ledger in under one second — creating an immutable, auditable proof of settlement finality. This closes the fraud and chargeback window that exists during the 3-5 day ACH settlement cycle, allowing processors to safely release funds immediately.

No customer PII is written to the blockchain. No existing payment rails are replaced.

## Core Capabilities

- **Instant refund initiation** — POST a refund request, receive a receipt with settlement reference
- **Kaspa blockchain anchoring** — cryptographic finality via distributed ledger confirmation
- **Compliance reporting** — PCI DSS / SOX-ready audit reports (JSON or CSV) per merchant per period
- **Acquirer normalization** — multi-acquirer support with flow position tracking
- **17 payment intelligence tools** — BIN lookup, IBAN validator, sanctions screening, fraud scoring, and more

## Tech Stack

- Python 3.11 + FastAPI + Uvicorn
- Rust sidecar (Kaspa signing service)
- PostgreSQL (DigitalOcean managed)
- Deployed on DigitalOcean App Platform

## API Endpoints

### Refunds
- `POST /v1/refunds/instant` — initiate an instant refund
- `GET /v1/refunds/{refund_id}` — look up refund status
- `POST /v1/refunds/refresh` — advance pending refund states

### Compliance
- `GET /v1/compliance/report` — generate PCI/SOX audit report (requires `X-API-Key`)

### Payment Intelligence Tools
BIN lookup, MCC lookup, IBAN validator, SWIFT lookup, currency converter, wallet validator, sanctions screening, PEP screening, routing validator, ISO 8583 parser, fraud scoring, token pricing, EIN validator, DeFi health, payment intelligence, payee verification (UK CoP / EU VoP)

## Authentication

All refund and compliance endpoints require an `X-API-Key` header.

## Deployment

Hosted on DigitalOcean App Platform (NYC region).  
GitHub: [enzokratko-CypherPunk/instant-refund](https://github.com/enzokratko-CypherPunk/instant-refund)

## About

Built by Brian Kratko, Settlement Assurance LLC  
Contact: brian@bmkdigitalsolutions.com
