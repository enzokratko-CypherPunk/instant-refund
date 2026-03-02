from typing import Dict, Any

SWIFT_DATA: Dict[str, Dict[str, str]] = {
    "CHASUS33": {"bank": "JPMorgan Chase Bank", "country_code": "US", "country": "United States", "city": "New York"},
    "BOFAUS3N": {"bank": "Bank of America", "country_code": "US", "country": "United States", "city": "Charlotte"},
    "WFBIUS6S": {"bank": "Wells Fargo Bank", "country_code": "US", "country": "United States", "city": "San Francisco"},
    "CITIUS33": {"bank": "Citibank", "country_code": "US", "country": "United States", "city": "New York"},
    "USBKUS44": {"bank": "U.S. Bank", "country_code": "US", "country": "United States", "city": "Minneapolis"},
    "PNCCUS33": {"bank": "PNC Bank", "country_code": "US", "country": "United States", "city": "Pittsburgh"},
    "TRWIUS33": {"bank": "Truist Bank", "country_code": "US", "country": "United States", "city": "Charlotte"},
    "KEYBUS33": {"bank": "KeyBank", "country_code": "US", "country": "United States", "city": "Cleveland"},
    "FNBOUS33": {"bank": "Fifth Third Bank", "country_code": "US", "country": "United States", "city": "Cincinnati"},
    "HATRUS31": {"bank": "HSBC Bank USA", "country_code": "US", "country": "United States", "city": "New York"},
    "MRMDUS33": {"bank": "M&T Bank", "country_code": "US", "country": "United States", "city": "Buffalo"},
    "SVBKUS6S": {"bank": "Silicon Valley Bank", "country_code": "US", "country": "United States", "city": "Santa Clara"},
    "GSCHUS33": {"bank": "Goldman Sachs Bank", "country_code": "US", "country": "United States", "city": "New York"},
    "MSNYUS33": {"bank": "Morgan Stanley", "country_code": "US", "country": "United States", "city": "New York"},
    "BARCGB22": {"bank": "Barclays Bank", "country_code": "GB", "country": "United Kingdom", "city": "London"},
    "NWBKGB2L": {"bank": "NatWest (Royal Bank of Scotland)", "country_code": "GB", "country": "United Kingdom", "city": "London"},
    "HBUKGB4B": {"bank": "HSBC UK Bank", "country_code": "GB", "country": "United Kingdom", "city": "London"},
    "LOYDGB2L": {"bank": "Lloyds Bank", "country_code": "GB", "country": "United Kingdom", "city": "London"},
    "SCBLGB2L": {"bank": "Standard Chartered Bank", "country_code": "GB", "country": "United Kingdom", "city": "London"},
    "BUKBGB22": {"bank": "Barclays UK", "country_code": "GB", "country": "United Kingdom", "city": "London"},
    "DEUTDEFF": {"bank": "Deutsche Bank", "country_code": "DE", "country": "Germany", "city": "Frankfurt"},
    "COBADEFF": {"bank": "Commerzbank", "country_code": "DE", "country": "Germany", "city": "Frankfurt"},
    "BNPAFRPP": {"bank": "BNP Paribas", "country_code": "FR", "country": "France", "city": "Paris"},
    "SOGEFRPP": {"bank": "Societe Generale", "country_code": "FR", "country": "France", "city": "Paris"},
    "CRLYFRPP": {"bank": "Credit Lyonnais (LCL)", "country_code": "FR", "country": "France", "city": "Paris"},
    "AGRIFRPP": {"bank": "Credit Agricole", "country_code": "FR", "country": "France", "city": "Paris"},
    "BCITITMM": {"bank": "Intesa Sanpaolo", "country_code": "IT", "country": "Italy", "city": "Milan"},
    "UNCRITMM": {"bank": "UniCredit", "country_code": "IT", "country": "Italy", "city": "Milan"},
    "BBVAESM": {"bank": "BBVA", "country_code": "ES", "country": "Spain", "city": "Madrid"},
    "CABORUMM": {"bank": "Raiffeisenbank", "country_code": "RU", "country": "Russia", "city": "Moscow"},
    "UBSWCHZH": {"bank": "UBS", "country_code": "CH", "country": "Switzerland", "city": "Zurich"},
    "CRESCHZZ": {"bank": "Credit Suisse", "country_code": "CH", "country": "Switzerland", "city": "Zurich"},
    "MABORUMM": {"bank": "Sberbank", "country_code": "RU", "country": "Russia", "city": "Moscow"},
    "ABNANL2A": {"bank": "ABN AMRO Bank", "country_code": "NL", "country": "Netherlands", "city": "Amsterdam"},
    "INGBNL2A": {"bank": "ING Bank", "country_code": "NL", "country": "Netherlands", "city": "Amsterdam"},
    "RABONL2U": {"bank": "Rabobank", "country_code": "NL", "country": "Netherlands", "city": "Utrecht"},
    "DABADKKK": {"bank": "Danske Bank", "country_code": "DK", "country": "Denmark", "city": "Copenhagen"},
    "NDEASESS": {"bank": "Nordea Bank", "country_code": "SE", "country": "Sweden", "city": "Stockholm"},
    "HANDSESS": {"bank": "Handelsbanken", "country_code": "SE", "country": "Sweden", "city": "Stockholm"},
    "DNBANOKK": {"bank": "DNB Bank", "country_code": "NO", "country": "Norway", "city": "Oslo"},
    "AABORUMM": {"bank": "Alfa-Bank", "country_code": "RU", "country": "Russia", "city": "Moscow"},
    "MABORUMM": {"bank": "Sberbank", "country_code": "RU", "country": "Russia", "city": "Moscow"},
    "SCBLHKHH": {"bank": "Standard Chartered Hong Kong", "country_code": "HK", "country": "Hong Kong", "city": "Hong Kong"},
    "HSBCHKHH": {"bank": "HSBC Hong Kong", "country_code": "HK", "country": "Hong Kong", "city": "Hong Kong"},
    "BKCHCNBJ": {"bank": "Bank of China", "country_code": "CN", "country": "China", "city": "Beijing"},
    "ICBKCNBJ": {"bank": "Industrial and Commercial Bank of China", "country_code": "CN", "country": "China", "city": "Beijing"},
    "CCBKCNBJ": {"bank": "China Construction Bank", "country_code": "CN", "country": "China", "city": "Beijing"},
    "MABORUMM": {"bank": "Sberbank", "country_code": "RU", "country": "Russia", "city": "Moscow"},
    "BOABORUMM": {"bank": "VTB Bank", "country_code": "RU", "country": "Russia", "city": "Moscow"},
    "MHCBJPJT": {"bank": "Mizuho Bank", "country_code": "JP", "country": "Japan", "city": "Tokyo"},
    "SMCEJPJT": {"bank": "Sumitomo Mitsui Banking", "country_code": "JP", "country": "Japan", "city": "Tokyo"},
    "BOTKJPJT": {"bank": "MUFG Bank", "country_code": "JP", "country": "Japan", "city": "Tokyo"},
    "ANZBAU3M": {"bank": "ANZ Bank", "country_code": "AU", "country": "Australia", "city": "Melbourne"},
    "CTBAAU2S": {"bank": "Commonwealth Bank of Australia", "country_code": "AU", "country": "Australia", "city": "Sydney"},
    "NABORUMM": {"bank": "National Bank of Australia", "country_code": "AU", "country": "Australia", "city": "Melbourne"},
    "WPACAU2S": {"bank": "Westpac Banking", "country_code": "AU", "country": "Australia", "city": "Sydney"},
    "BKDNINBB": {"bank": "Bank of India", "country_code": "IN", "country": "India", "city": "Mumbai"},
    "SBININBB": {"bank": "State Bank of India", "country_code": "IN", "country": "India", "city": "Mumbai"},
    "HDFCINBB": {"bank": "HDFC Bank", "country_code": "IN", "country": "India", "city": "Mumbai"},
    "ABORUMM": {"bank": "Alfa-Bank", "country_code": "RU", "country": "Russia", "city": "Moscow"},
    "BOFSGB2S": {"bank": "Bank of Scotland", "country_code": "GB", "country": "United Kingdom", "city": "Edinburgh"},
    "ROYCCAT2": {"bank": "Royal Bank of Canada", "country_code": "CA", "country": "Canada", "city": "Toronto"},
    "TDOMCATT": {"bank": "TD Bank", "country_code": "CA", "country": "Canada", "city": "Toronto"},
    "BNDCCAMM": {"bank": "Bank of Nova Scotia (Scotiabank)", "country_code": "CA", "country": "Canada", "city": "Toronto"},
    "CABORUMM": {"bank": "CIBC", "country_code": "CA", "country": "Canada", "city": "Toronto"},
    "BMOOCA": {"bank": "Bank of Montreal", "country_code": "CA", "country": "Canada", "city": "Montreal"},
    "ADCBAEAA": {"bank": "Abu Dhabi Commercial Bank", "country_code": "AE", "country": "United Arab Emirates", "city": "Abu Dhabi"},
    "ABORUMM": {"bank": "Alfa-Bank", "country_code": "RU", "country": "Russia", "city": "Moscow"},
    "NBABORUMM": {"bank": "National Bank of Abu Dhabi", "country_code": "AE", "country": "United Arab Emirates", "city": "Abu Dhabi"},
    "SAMBSARI": {"bank": "Samba Financial Group", "country_code": "SA", "country": "Saudi Arabia", "city": "Riyadh"},
    "RIABORUMM": {"bank": "Riyad Bank", "country_code": "SA", "country": "Saudi Arabia", "city": "Riyadh"},
}

COUNTRY_CODES: Dict[str, str] = {
    "US": "United States", "GB": "United Kingdom", "DE": "Germany", "FR": "France",
    "IT": "Italy", "ES": "Spain", "CH": "Switzerland", "NL": "Netherlands",
    "BE": "Belgium", "AT": "Austria", "SE": "Sweden", "NO": "Norway",
    "DK": "Denmark", "FI": "Finland", "IE": "Ireland", "PT": "Portugal",
    "GR": "Greece", "PL": "Poland", "CZ": "Czech Republic", "HU": "Hungary",
    "RO": "Romania", "BG": "Bulgaria", "HR": "Croatia", "SK": "Slovakia",
    "SI": "Slovenia", "LT": "Lithuania", "LV": "Latvia", "EE": "Estonia",
    "CY": "Cyprus", "MT": "Malta", "LU": "Luxembourg", "RU": "Russia",
    "CN": "China", "JP": "Japan", "KR": "South Korea", "IN": "India",
    "AU": "Australia", "NZ": "New Zealand", "CA": "Canada", "MX": "Mexico",
    "BR": "Brazil", "AR": "Argentina", "ZA": "South Africa", "AE": "United Arab Emirates",
    "SA": "Saudi Arabia", "HK": "Hong Kong", "SG": "Singapore", "TW": "Taiwan",
    "TH": "Thailand", "MY": "Malaysia", "ID": "Indonesia", "PH": "Philippines",
    "TR": "Turkey", "IL": "Israel", "EG": "Egypt", "NG": "Nigeria",
    "KE": "Kenya", "GH": "Ghana", "TZ": "Tanzania",
}

def lookup_swift(swift_code: str) -> Dict[str, Any]:
    clean = swift_code.strip().upper().replace(" ", "")

    if len(clean) not in (8, 11):
        return {"status": "error", "error": "SWIFT/BIC must be 8 or 11 characters", "swift": swift_code}

    if not clean[:6].isalpha():
        return {"status": "error", "error": "First 6 characters must be letters", "swift": clean}

    bank_code = clean[:4]
    country_code = clean[4:6]
    location_code = clean[6:8]
    branch_code = clean[8:] if len(clean) == 11 else "XXX (Head Office)"

    base_code = clean[:8]

    if base_code in SWIFT_DATA:
        data = SWIFT_DATA[base_code]
        return {
            "status": "success",
            "swift": clean,
            "bank_code": bank_code,
            "country_code": country_code,
            "country_name": data["country"],
            "location_code": location_code,
            "branch_code": branch_code,
            "bank_name": data["bank"],
            "city": data["city"],
        }

    country_name = COUNTRY_CODES.get(country_code, "Unknown")
    return {
        "status": "partial",
        "swift": clean,
        "bank_code": bank_code,
        "country_code": country_code,
        "country_name": country_name,
        "location_code": location_code,
        "branch_code": branch_code,
        "bank_name": "Unknown - not in database",
        "city": "Unknown",
    }
