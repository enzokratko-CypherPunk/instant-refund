import httpx
from typing import Dict, Any
import re

EIN_PATTERN = re.compile(r'^\d{2}-?\d{7}$')

KNOWN_ENTITY_TYPES = {
    "LLC": "Limited Liability Company",
    "INC": "Corporation",
    "CORP": "Corporation",
    "LTD": "Limited Company",
    "LP": "Limited Partnership",
    "LLP": "Limited Liability Partnership",
    "PC": "Professional Corporation",
    "DBA": "Doing Business As",
    "NA": "National Association (Bank)",
    "FSB": "Federal Savings Bank",
}

def detect_entity_type(name: str) -> str:
    if not name:
        return "Unknown"
    name_upper = name.upper()
    for suffix, label in KNOWN_ENTITY_TYPES.items():
        if name_upper.endswith(f" {suffix}") or f" {suffix}," in name_upper:
            return label
    return "Unknown"

def validate_ein(ein: str) -> Dict[str, Any]:
    ein_clean = ein.strip().replace("-", "")
    
    if not EIN_PATTERN.match(ein.strip()):
        return {"status": "error", "message": "Invalid EIN format. Expected XX-XXXXXXX or XXXXXXXXX."}
    
    if len(ein_clean) != 9:
        return {"status": "error", "message": "EIN must be exactly 9 digits."}

    prefix = int(ein_clean[:2])
    
    # IRS-assigned EIN prefix ranges
    VALID_PREFIXES = list(range(1, 10)) + list(range(10, 40)) + list(range(40, 60)) + \
                     list(range(60, 80)) + list(range(80, 100))
    INVALID_PREFIXES = [0, 7, 8, 9, 17, 18, 19, 28, 29, 49, 69, 70, 78, 79, 89]

    is_valid = prefix not in INVALID_PREFIXES and prefix in VALID_PREFIXES

    # Campus assignments
    CAMPUS_MAP = {
        (1, 6): "Andover, MA",
        (10, 16): "Austin, TX",
        (20, 27): "Cincinnati, OH",
        (30, 32): "Atlanta, GA",
        (33, 39): "Philadelphia, PA",
        (40, 48): "Kansas City, MO",
        (50, 58): "Ogden, UT",
        (59, 65): "Brookhaven, NY",
        (66, 68): "Memphis, TN",
        (71, 77): "Fresno, CA",
        (80, 88): "Ogden, UT",
        (90, 99): "Ogden, UT",
    }

    issuing_campus = "Unknown"
    for (low, high), campus in CAMPUS_MAP.items():
        if low <= prefix <= high:
            issuing_campus = campus
            break

    return {
        "status": "success",
        "ein": f"{ein_clean[:2]}-{ein_clean[2:]}",
        "valid": is_valid,
        "prefix": ein_clean[:2],
        "issuing_campus": issuing_campus,
        "format_check": "passed",
        "note": "EIN format and prefix validated against IRS assignment rules. Live IRS verification requires direct IRS API access."
    }
