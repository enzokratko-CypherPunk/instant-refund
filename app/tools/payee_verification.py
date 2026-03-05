from typing import Dict, Any
import re

UK_SORT_CODE_PATTERN = re.compile(r'^\d{2}-?\d{2}-?\d{2}$')
UK_ACCOUNT_PATTERN = re.compile(r'^\d{8}$')
IBAN_PATTERN = re.compile(r'^[A-Z]{2}\d{2}[A-Z0-9]{4,}$')

COP_MATCH_RULES = {
    "full_match": {"code": "MATC", "status": "MATCHED", "confidence": 100},
    "close_match": {"code": "CLOM", "status": "CLOSE MATCH", "confidence": 75},
    "no_match": {"code": "NOMA", "status": "NOT MATCHED", "confidence": 0},
    "unavailable": {"code": "ISC", "status": "UNAVAILABLE", "confidence": -1},
}

EU_VOP_RULES = {
    "matched": {"result": "VERIFICATION_PASSED", "confidence": 100},
    "not_matched": {"result": "VERIFICATION_FAILED", "confidence": 0},
    "partial": {"result": "PARTIAL_MATCH", "confidence": 60},
    "unavailable": {"result": "UNABLE_TO_VERIFY", "confidence": -1},
}

SUPPORTED_EU_COUNTRIES = [
    "DE", "FR", "NL", "BE", "IT", "ES", "AT", "PT", "FI", "IE",
    "LU", "LT", "LV", "EE", "SK", "SI", "MT", "CY", "GR", "HR"
]

def validate_uk_cop(
    sort_code: str,
    account_number: str,
    account_name: str,
    account_type: str = "personal"
) -> Dict[str, Any]:
    sort_clean = sort_code.strip().replace("-", "").replace(" ", "")
    account_clean = account_number.strip().replace(" ", "")

    errors = []
    if not re.match(r'^\d{6}$', sort_clean):
        errors.append("Invalid sort code format. Expected 6 digits (e.g. 20-00-00 or 200000).")
    if not re.match(r'^\d{8}$', account_clean):
        errors.append("Invalid account number. Expected 8 digits.")
    if not account_name or len(account_name.strip()) < 2:
        errors.append("Account name is required.")

    if errors:
        return {"status": "error", "errors": errors}

    formatted_sort = f"{sort_clean[:2]}-{sort_clean[2:4]}-{sort_clean[4:]}"
    name_words = account_name.strip().upper().split()
    is_business = account_type.lower() == "business"

    mock_result = COP_MATCH_RULES["full_match"]
    match_note = "Simulated COP response. In production, this calls the Pay.UK Confirmation of Payee service."

    if len(account_name.strip()) < 4:
        mock_result = COP_MATCH_RULES["close_match"]
    if sort_clean.startswith("00"):
        mock_result = COP_MATCH_RULES["unavailable"]

    return {
        "status": "success",
        "scheme": "UK_COP",
        "validation": {
            "sort_code": formatted_sort,
            "account_number": account_clean,
            "account_name": account_name.strip(),
            "account_type": account_type.lower(),
            "format_valid": True
        },
        "cop_response": {
            "match_code": mock_result["code"],
            "match_status": mock_result["status"],
            "confidence_score": mock_result["confidence"],
            "name_checked": account_name.strip(),
            "is_business": is_business
        },
        "note": match_note,
        "data_source": "Format validation + simulated COP response"
    }

def validate_eu_vop(
    iban: str,
    account_name: str
) -> Dict[str, Any]:
    iban_clean = iban.strip().upper().replace(" ", "")

    errors = []
    if len(iban_clean) < 15 or len(iban_clean) > 34:
        errors.append("Invalid IBAN length.")
    if not re.match(r'^[A-Z]{2}\d{2}[A-Z0-9]+$', iban_clean):
        errors.append("Invalid IBAN format.")
    if not account_name or len(account_name.strip()) < 2:
        errors.append("Account name is required.")

    if errors:
        return {"status": "error", "errors": errors}

    country_code = iban_clean[:2]
    supported = country_code in SUPPORTED_EU_COUNTRIES
    mock_result = EU_VOP_RULES["matched"] if supported else EU_VOP_RULES["unavailable"]

    return {
        "status": "success",
        "scheme": "EU_VOP",
        "validation": {
            "iban": iban_clean,
            "country_code": country_code,
            "account_name": account_name.strip(),
            "format_valid": True,
            "sepa_supported": supported
        },
        "vop_response": {
            "verification_result": mock_result["result"],
            "confidence_score": mock_result["confidence"],
            "name_checked": account_name.strip(),
            "country_supported": supported
        },
        "note": "Simulated VOP response. In production this calls the SEPA VOP scheme via your PSP.",
        "data_source": "Format validation + simulated EU VOP response"
    }
