from typing import Dict, Any, Optional
from app.tools.bin_lookup import lookup_bin
from app.tools.decline_codes import interpret_decline
from app.tools.mcc_lookup import lookup_mcc
from app.tools.fraud_score import calculate_fraud_score

RETRY_MATRIX = {
    "do_not_retry": {
        "codes": ["14", "41", "43", "54", "57", "62", "93", "R0", "R1", "R2", "R3"],
        "window_minutes": 0,
        "probability": 0,
        "advice": "Do not retry. Card permanently blocked or fraud confirmed."
    },
    "retry_immediately": {
        "codes": ["91", "96", "N7", "Z3"],
        "window_minutes": 5,
        "probability": 75,
        "advice": "Issuer temporarily unavailable. Retry within 5 minutes."
    },
    "retry_later": {
        "codes": ["51", "61", "65"],
        "window_minutes": 1440,
        "probability": 55,
        "advice": "Insufficient funds or limit exceeded. Retry after 24 hours."
    },
    "retry_with_auth": {
        "codes": ["59", "63", "70", "71", "75", "1A", "6P"],
        "window_minutes": 30,
        "probability": 60,
        "advice": "Authentication required. Retry with 3DS or step-up verification."
    },
    "contact_bank": {
        "codes": ["05", "12", "15", "58", "76", "78"],
        "window_minutes": 0,
        "probability": 20,
        "advice": "Issuer declined without clear reason. Cardholder should contact bank."
    },
}

HIGH_RISK_MCC = {
    "7995": "Gambling",
    "5912": "Drug Stores/Pharmacies",
    "5999": "Miscellaneous Retail",
    "4829": "Wire Transfer",
    "6051": "Crypto/Non-Financial Institutions",
    "7273": "Dating Services",
    "5962": "Direct Marketing",
}

def get_retry_strategy(decline_code: str) -> Dict[str, Any]:
    for strategy, data in RETRY_MATRIX.items():
        if decline_code.upper() in [c.upper() for c in data["codes"]]:
            return {
                "strategy": strategy,
                "retry_window_minutes": data["window_minutes"],
                "retry_probability_pct": data["probability"],
                "retry_advice": data["advice"]
            }
    return {
        "strategy": "retry_later",
        "retry_window_minutes": 60,
        "retry_probability_pct": 40,
        "retry_advice": "Unknown decline code. Wait 60 minutes before retrying."
    }

def get_amount_risk(amount: float, mcc: str) -> Dict[str, Any]:
    risk_flags = []
    if amount > 5000:
        risk_flags.append("High-value transaction — enhanced monitoring recommended")
    if amount < 1.00:
        risk_flags.append("Micro-transaction — possible card testing pattern")
    if mcc in HIGH_RISK_MCC:
        risk_flags.append(f"High-risk merchant category: {HIGH_RISK_MCC[mcc]}")
    return {
        "amount_risk_flags": risk_flags if risk_flags else ["No amount-based risk flags"],
        "high_risk_mcc": mcc in HIGH_RISK_MCC
    }

def build_recommendation(
    retry_strategy: str,
    fraud_risk_level: str,
    retry_probability: int,
    amount_flags: list
) -> str:
    if fraud_risk_level in ["HIGH", "MEDIUM-HIGH"] and retry_strategy == "do_not_retry":
        return "BLOCK: High fraud risk combined with hard decline. Do not retry under any circumstances."
    if fraud_risk_level == "HIGH":
        return "REVIEW: High fraud risk detected. Require step-up authentication before any retry attempt."
    if retry_strategy == "do_not_retry":
        return "DECLINE: Hard decline code. Do not retry this transaction."
    if retry_probability >= 70:
        return "RETRY: High probability of success on retry. Proceed as advised."
    if retry_probability >= 40:
        return "RETRY WITH CAUTION: Moderate retry probability. Monitor for fraud patterns."
    return "HOLD: Low retry probability. Wait for cardholder to resolve with their bank."

async def analyze_payment(
    card_bin: str,
    decline_code: str,
    merchant_mcc: str,
    transaction_amount: float,
    country_code: str = "US",
    card_type: str = "credit",
    network: str = "Visa"
) -> Dict[str, Any]:

    # Pull from existing tools
    bin_data = lookup_bin(card_bin) if card_bin else {}
    decline_data = interpret_decline(decline_code) if decline_code else {}
    mcc_data = lookup_mcc(merchant_mcc) if merchant_mcc else {}

    # Use BIN data if available
    resolved_card_type = bin_data.get("card_type", card_type) or card_type
    resolved_network = bin_data.get("network", network) or network
    resolved_country = bin_data.get("country_code", country_code) or country_code

    fraud_data = calculate_fraud_score(
        card_type=resolved_card_type,
        network=resolved_network,
        country_code=resolved_country,
        is_commercial=bin_data.get("is_commercial", False),
        is_anonymous=False
    )

    retry = get_retry_strategy(decline_code)
    amount_risk = get_amount_risk(transaction_amount, merchant_mcc)
    recommendation = build_recommendation(
        retry["strategy"],
        fraud_data["risk_level"],
        retry["retry_probability_pct"],
        amount_risk["amount_risk_flags"]
    )

    return {
        "status": "success",
        "recommendation": recommendation,
        "retry": {
            "strategy": retry["strategy"],
            "probability_pct": retry["retry_probability_pct"],
            "window_minutes": retry["retry_window_minutes"],
            "advice": retry["retry_advice"]
        },
        "fraud": {
            "score": fraud_data["fraud_score"],
            "risk_level": fraud_data["risk_level"],
            "risk_factors": fraud_data["risk_factors"]
        },
        "decline": {
            "code": decline_code,
            "meaning": decline_data.get("meaning", "Unknown"),
            "category": decline_data.get("category", "Unknown"),
            "retryable": decline_data.get("retryable", "Unknown")
        },
        "card": {
            "bin": card_bin,
            "network": resolved_network,
            "card_type": resolved_card_type,
            "issuing_country": resolved_country,
            "bank": bin_data.get("bank_name", "Unknown")
        },
        "merchant": {
            "mcc": merchant_mcc,
            "category": mcc_data.get("description", "Unknown"),
            "high_risk": amount_risk["high_risk_mcc"]
        },
        "transaction": {
            "amount": transaction_amount,
            "risk_flags": amount_risk["amount_risk_flags"]
        },
        "data_sources": ["Internal BIN DB", "OFAC Logic", "IRS Prefix Rules", "Payments Domain Intelligence"]
    }
