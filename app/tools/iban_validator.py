from typing import Dict, Any

IBAN_LENGTHS: Dict[str, int] = {
    "AL": 28, "AD": 24, "AT": 20, "AZ": 28, "BH": 22, "BY": 28, "BE": 16,
    "BA": 20, "BR": 29, "BG": 22, "CR": 22, "HR": 21, "CY": 28, "CZ": 24,
    "DK": 18, "DO": 28, "TL": 23, "EE": 20, "FO": 18, "FI": 18, "FR": 27,
    "GE": 22, "DE": 22, "GI": 23, "GR": 27, "GL": 18, "GT": 28, "HU": 28,
    "IS": 26, "IQ": 23, "IE": 22, "IL": 23, "IT": 27, "JO": 30, "KZ": 20,
    "XK": 20, "KW": 30, "LV": 21, "LB": 28, "LI": 21, "LT": 20, "LU": 20,
    "MK": 19, "MT": 31, "MR": 27, "MU": 30, "MC": 27, "MD": 24, "ME": 22,
    "NL": 18, "NO": 15, "PK": 24, "PS": 29, "PL": 28, "PT": 25, "QA": 29,
    "RO": 24, "LC": 32, "SM": 27, "ST": 25, "SA": 24, "RS": 22, "SC": 31,
    "SK": 24, "SI": 19, "ES": 24, "SE": 24, "CH": 21, "TN": 24, "TR": 26,
    "UA": 29, "AE": 23, "GB": 22, "VA": 22, "VG": 24,
}

COUNTRY_NAMES: Dict[str, str] = {
    "AL": "Albania", "AD": "Andorra", "AT": "Austria", "AZ": "Azerbaijan",
    "BH": "Bahrain", "BY": "Belarus", "BE": "Belgium", "BA": "Bosnia and Herzegovina",
    "BR": "Brazil", "BG": "Bulgaria", "CR": "Costa Rica", "HR": "Croatia",
    "CY": "Cyprus", "CZ": "Czech Republic", "DK": "Denmark", "DO": "Dominican Republic",
    "TL": "East Timor", "EE": "Estonia", "FO": "Faroe Islands", "FI": "Finland",
    "FR": "France", "GE": "Georgia", "DE": "Germany", "GI": "Gibraltar",
    "GR": "Greece", "GL": "Greenland", "GT": "Guatemala", "HU": "Hungary",
    "IS": "Iceland", "IQ": "Iraq", "IE": "Ireland", "IL": "Israel",
    "IT": "Italy", "JO": "Jordan", "KZ": "Kazakhstan", "XK": "Kosovo",
    "KW": "Kuwait", "LV": "Latvia", "LB": "Lebanon", "LI": "Liechtenstein",
    "LT": "Lithuania", "LU": "Luxembourg", "MK": "North Macedonia", "MT": "Malta",
    "MR": "Mauritania", "MU": "Mauritius", "MC": "Monaco", "MD": "Moldova",
    "ME": "Montenegro", "NL": "Netherlands", "NO": "Norway", "PK": "Pakistan",
    "PS": "Palestine", "PL": "Poland", "PT": "Portugal", "QA": "Qatar",
    "RO": "Romania", "LC": "Saint Lucia", "SM": "San Marino", "ST": "Sao Tome",
    "SA": "Saudi Arabia", "RS": "Serbia", "SC": "Seychelles", "SK": "Slovakia",
    "SI": "Slovenia", "ES": "Spain", "SE": "Sweden", "CH": "Switzerland",
    "TN": "Tunisia", "TR": "Turkey", "UA": "Ukraine", "AE": "United Arab Emirates",
    "GB": "United Kingdom", "VA": "Vatican City", "VG": "British Virgin Islands",
}

def _mod97(iban_digits: str) -> int:
    remainder = 0
    for ch in iban_digits:
        remainder = (remainder * 10 + int(ch)) % 97
    return remainder

def validate_iban(iban: str) -> Dict[str, Any]:
    clean = iban.replace(" ", "").replace("-", "").upper()

    if len(clean) < 5:
        return {"status": "error", "error": "IBAN too short", "iban": iban}

    country_code = clean[:2]
    check_digits = clean[2:4]
    bban = clean[4:]

    if country_code not in IBAN_LENGTHS:
        return {"status": "error", "error": f"Unknown country code: {country_code}", "iban": clean}

    expected_len = IBAN_LENGTHS[country_code]
    if len(clean) != expected_len:
        return {"status": "error", "error": f"Invalid length: expected {expected_len}, got {len(clean)}", "iban": clean}

    rearranged = clean[4:] + clean[:4]
    numeric = ""
    for ch in rearranged:
        if ch.isdigit():
            numeric += ch
        else:
            numeric += str(ord(ch) - 55)

    if _mod97(numeric) != 1:
        return {"status": "error", "error": "Checksum validation failed", "iban": clean}

    country_name = COUNTRY_NAMES.get(country_code, "Unknown")
    bank_code = bban[:4] if len(bban) >= 4 else bban

    return {
        "status": "success",
        "iban": clean,
        "valid": True,
        "country_code": country_code,
        "country_name": country_name,
        "check_digits": check_digits,
        "bank_code": bank_code,
        "bban": bban,
    }
