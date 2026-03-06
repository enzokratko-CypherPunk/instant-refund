# Post 1: r/fintech

## Kratko Fintech Tools — 15 APIs for Payment & Compliance Infrastructure

We built a set of fintech developer APIs focused on the parsing, validation, and risk assessment work that most payment platforms need but don't want to solve in-house. Launching public beta today.

**What we have:**

- **BIN Lookup API** — Identify issuer bank, network, card type, and country from the first 6-8 digits.
- **MCC Lookup API** — Decode any 4-digit Merchant Category Code into a human-readable category and description.
- **IBAN Validator API** — Validate IBAN checksum and parse country, bank, and account components.
- **Decline Code Interpreter API** — Translate any payment decline code into plain-English meaning, category, and retry guidance.
- **SWIFT BIC Lookup API** — Validate and decode any SWIFT/BIC code into bank name, country, city, and branch.
- **Currency Converter API** — Real-time currency conversion across 150+ currencies.
- **Crypto Wallet Address Validator API** — Validate crypto wallet addresses across 20+ blockchain networks including Bitcoin, Ethereum, Solana, and Kaspa.
- **Sanctions Checker API** — Screen names and entities against the OFAC SDN list with fuzzy matching.
- **PEP Screener API** — Screen individuals against politically exposed persons databases for KYC/AML compliance.
- **Routing Number Validator API** — Validate US ABA routing numbers and identify the issuing bank and Federal Reserve district.
- **ISO 8583 Parser API** — Parse raw ISO 8583 financial transaction messages into structured JSON with human-readable field enrichment.
- **Card Fraud Score API** — Score payment card fraud risk based on card type, network, issuing country, and card attributes.
- **Token Price Feed API** — Real-time cryptocurrency prices with 24h change, market cap, and volume for 25+ tokens.
- **EIN Validator API** — Validate US Employer Identification Numbers against IRS prefix assignment rules.
- **DeFi Health Checker API** — Real-time DeFi protocol health monitoring — TVL, 24h change, and risk assessment for 15 major protocols.
- **Payment Intelligence API** — Full-spectrum payment analysis — input BIN, decline code, MCC, and amount to get retry strategy, fraud risk, and plain-English recommendation.

**Free tier & rate limits:**

Free tier includes request-based quotas and fair-use rate limiting. Limits scale with plan tier. Pricing available on docs.

**Base endpoint:** https://instant-refund-api-l99qr.ondigitalocean.app

**What we're looking for:**

- Are any of these actually useful for your stack, or do we solve a problem you don't have?
- What's missing? (e.g., BVN validation, additional crypto networks, real-time KYC integrations)
- What's your friction with current third-party fintech APIs—speed, accuracy, pricing, documentation?

Feedback welcome. API docs linked in profile or at the base URL.

---

# Post 2: r/webdev

## Launched: Kratko Fintech APIs — Payment data parsing & compliance screening

Built a suite of 15 APIs for payment and compliance work. We know most of you aren't building fintech-specific products, but if you're integrating payments, handling card data, currency conversion, or doing KYC checks, these might save integration time.

**Quick rundown:**

- **BIN Lookup API** — Identify issuer bank, network, card type, and country from the first 6-8 digits.
- **MCC Lookup API** — Decode any 4-digit Merchant Category Code into a human-readable category and description.
- **IBAN Validator API** — Validate IBAN checksum and parse country, bank, and account components.
- **Decline Code Interpreter API** — Translate any payment decline code into plain-English meaning, category, and retry guidance.
- **SWIFT BIC Lookup API** — Validate and decode any SWIFT/BIC code into bank name, country, city, and branch.
- **Currency Converter API** — Real-time currency conversion across 150+ currencies.
- **Crypto Wallet Address Validator API** — Validate crypto wallet addresses across 20+ blockchain networks including Bitcoin, Ethereum, Solana, and Kaspa.
- **Sanctions Checker API** — Screen names and entities against the OFAC SDN list with fuzzy matching.
- **PEP Screener API** — Screen individuals against politically exposed persons databases for KYC/AML compliance.
- **Routing Number Validator API** — Validate US ABA routing numbers and identify the issuing bank and Federal Reserve district.
- **ISO 8583 Parser API** — Parse raw ISO 8583 financial transaction messages into structured JSON with human-readable field enrichment.
- **Card Fraud Score API** — Score payment card fraud risk based on card type, network, issuing country, and card attributes.
- **Token Price Feed API** — Real-time cryptocurrency prices with 24h change, market cap, and volume for 25+ tokens.
- **EIN Validator API** — Validate US Employer Identification Numbers against IRS prefix assignment rules.
- **DeFi Health Checker API** — Real-time DeFi protocol health monitoring — TVL, 24h change, and risk assessment for 15 major protocols.
- **Payment Intelligence API** — Full-spectrum payment analysis — input BIN, decline code, MCC, and amount to get retry strategy, fraud risk, and plain-English recommendation.

**Free tier & rate limits:**

Free tier includes request-based quotas and fair-use rate limiting. Limits scale with plan tier. Details in docs.

**Endpoint:** https://instant-refund-api-l99qr.ondigitalocean.app

**Tell us:**

- Which of these would actually be useful in your projects?
- What's annoying about the payment/compliance APIs you use now?
- Missing anything obvious?

Open to honest feedback.