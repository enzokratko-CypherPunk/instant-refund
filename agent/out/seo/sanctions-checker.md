# Sanctions Checker API -- OFAC Sanctions API: Real-Time SDN List Screening

## Summary
Sanctions Checker API screens names against OFAC Specially Designated Nationals list in real-time. Fuzzy matching detects name variations and aliases. Essential for fintech, payments, and banking compliance workflows.

## Why developers use this
['Customer onboarding sanctions screening (KYC/AML)', 'Transaction monitoring and payment block prevention', 'Third-party vendor risk assessment', 'Automated compliance reporting for regulated entities', 'Cross-border remittance screening', 'Regulatory audit trail generation']

## API example
POST /v1/tools/sanctions/check with {'name': 'Ahmad Hassan Mohammad'} returns match=true, score=0.87, with OFAC aliases and entity details for compliance teams to investigate.

## FAQs
[{'q': 'Does this API check other sanctions lists besides OFAC?', 'a': 'Currently checks OFAC SDN list. Enterprise plans include EU, UK, UN, and FATF watchlists.'}, {'q': 'How does fuzzy matching improve detection?', 'a': 'Fuzzy matching catches misspellings, transliteration variants, and name format differences—critical for international names and aliases.'}, {'q': 'What confidence score indicates a true match?', 'a': 'Scores 0.85+ warrant manual review. 0.95+ typically require escalation. Configure thresholds per your compliance policy.'}, {'q': 'Is this API compliant with regulatory requirements?', 'a': 'Yes. Designed for FinCEN, Treasury, and banking regulatory compliance. Generates audit-ready logs for each screening.'}, {'q': "What's the typical response time?", 'a': '< 200ms per request. Handles 10K+ daily screenings for mid-market fintechs.'}]

## Keywords
['ofac sanctions api', 'sanctions screening api', 'aml check api', 'sdn list screening', 'ofac sdl lookup', 'compliance screening api', 'sanctions database api', 'kyc aml api', 'fintech sanctions check', 'name matching sanctions', 'fuzzy matching compliance', 'ofac api integration', 'sanctions monitoring api', 'regulatory screening api', 'anti-money laundering api']