from typing import Dict, Any

COUNTRY_RISK: Dict[str, int] = {
    "US": 10, "CA": 10, "GB": 10, "AU": 10, "DE": 10, "FR": 10, "NL": 10,
    "SE": 10, "NO": 10, "DK": 10, "FI": 10, "CH": 10, "AT": 10, "NZ": 10,
    "JP": 15, "KR": 15, "SG": 15, "HK": 15, "IE": 15, "BE": 15, "IT": 20,
    "ES": 20, "PT": 20, "GR": 25, "PL": 25, "CZ": 25, "HU": 25, "RO": 30,
    "BR": 40, "MX": 40, "AR": 45, "CO": 45, "ZA": 45, "IN": 35, "CN": 40,
    "RU": 70, "NG": 70, "GH": 65, "KE": 60, "PK": 65, "BD": 60, "VN": 50,
    "ID": 45, "PH": 50, "UA": 55, "BY": 65, "IQ": 75, "IR": 80, "SY": 80,
    "KP": 90, "CU": 80, "VE": 70, "MM": 65, "AF": 80,
}

NETWORK_RISK: Dict[str, int] = {
    "Visa": 5, "Mastercard": 5, "American Express": 5, "Discover": 5,
    "JCB": 10, "UnionPay": 20, "Maestro": 10, "Diners Club": 10,
    "Unknown": 30,
}

CARD_TYPE_RISK: Dict[str, int] = {
    "credit": 10, "debit": 5, "prepaid": 35, "charge": 10, "unknown": 20,
}

def calculate_fraud_score(
    card_type: str,
    network: str,
    country_code: str,
    is_commercial: bool = False,
    is_anonymous: bool = False,
) -> Dict[str, Any]:

    country_score = COUNTRY_RISK.get(country_code.upper() if country_code else "US", 40)
    network_score = NETWORK_RISK.get(network, 30)
    type_score = CARD_TYPE_RISK.get(card_type.lower() if card_type else "unknown", 20)

    commercial_bonus = 10 if is_commercial else 0
    anonymous_bonus = 25 if is_anonymous else 0

    raw_score = (country_score * 0.45) + (type_score * 0.30) + (network_score * 0.15) + (commercial_bonus * 0.05) + (anonymous_bonus * 0.05)
    fraud_score = min(100, round(raw_score))

    if fraud_score <= 20:
        risk_level = "LOW"
        recommendation = "Approve"
        explanation = "Card profile matches low-risk characteristics."
    elif fraud_score <= 40:
        risk_level = "MEDIUM-LOW"
        recommendation = "Approve with standard monitoring"
        explanation = "Minor risk indicators present. Standard fraud monitoring recommended."
    elif fraud_score <= 60:
        risk_level = "MEDIUM"
        recommendation = "Approve with enhanced monitoring"
        explanation = "Moderate risk indicators. Consider step-up authentication."
    elif fraud_score <= 75:
        risk_level = "MEDIUM-HIGH"
        recommendation = "Review before approval"
        explanation = "Multiple risk indicators. Manual review or 3DS authentication recommended."
    else:
        risk_level = "HIGH"
        recommendation = "Decline or require additional verification"
        explanation = "High-risk card profile. Strong authentication or decline recommended."

    factors = []
    if country_score >= 60:
        factors.append(f"High-risk issuing country ({country_code})")
    if card_type.lower() == "prepaid":
        factors.append("Prepaid card - higher fraud rate")
    if network in ["UnionPay", "Unknown"]:
        factors.append(f"Higher-risk network ({network})")
    if is_commercial:
        factors.append("Commercial card - elevated chargeback risk")
    if is_anonymous:
        factors.append("Anonymous/virtual card")
    if not factors:
        factors.append("No significant risk factors detected")

    return {
        "status": "success",
        "fraud_score": fraud_score,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "explanation": explanation,
        "risk_factors": factors,
        "score_components": {
            "country_risk": country_score,
            "card_type_risk": type_score,
            "network_risk": network_score,
            "commercial_bonus": commercial_bonus,
            "anonymous_bonus": anonymous_bonus,
        }
    }
