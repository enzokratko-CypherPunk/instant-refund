from typing import Dict, Any

BIN_DATA: Dict[str, Dict[str, str]] = {
    "411111": {"bank": "JPMorgan Chase", "brand": "Visa", "type": "Credit", "country": "US"},
    "444444": {"bank": "Bank of America", "brand": "Visa", "type": "Debit", "country": "US"},
    "510510": {"bank": "Capital One", "brand": "Mastercard", "type": "Credit", "country": "US"},
    "371234": {"bank": "American Express", "brand": "Amex", "type": "Charge", "country": "US"},
    "601100": {"bank": "Discover", "brand": "Discover", "type": "Credit", "country": "US"},
    "353011": {"bank": "JCB Co", "brand": "JCB", "type": "Credit", "country": "JP"},
}

def get_bin_details(bin_code: str) -> Dict[str, Any]:
    digits = "".join([c for c in (bin_code or "") if c.isdigit()])
    clean_bin = digits[:6]

    if len(clean_bin) < 6:
        return {"status": "error", "error": "BIN must contain at least 6 digits", "bin": clean_bin}

    if clean_bin in BIN_DATA:
        data = BIN_DATA[clean_bin]
        return {"status": "success", "bin": clean_bin, "bank": data["bank"], "brand": data["brand"], "type": data["type"], "country": data["country"]}

    return {"status": "partial_match", "bin": clean_bin, "bank": "Unknown Issuer", "brand": "Unknown", "type": "Unknown", "country": "Unknown"}
