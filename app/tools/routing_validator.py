from typing import Dict, Any

ROUTING_NUMBERS: Dict[str, Dict] = {
    "021000021": {"bank": "JPMorgan Chase Bank", "city": "Tampa", "state": "FL", "type": "ABA"},
    "021000089": {"bank": "Citibank", "city": "New York", "state": "NY", "type": "ABA"},
    "021001208": {"bank": "Bank of America", "city": "New York", "state": "NY", "type": "ABA"},
    "021100361": {"bank": "TD Bank", "city": "Lewiston", "state": "ME", "type": "ABA"},
    "021200339": {"bank": "Goldman Sachs Bank", "city": "New York", "state": "NY", "type": "ABA"},
    "021200025": {"bank": "HSBC Bank USA", "city": "Buffalo", "state": "NY", "type": "ABA"},
    "021300077": {"bank": "Santander Bank", "city": "East Providence", "state": "RI", "type": "ABA"},
    "022000020": {"bank": "KeyBank", "city": "Albany", "state": "NY", "type": "ABA"},
    "031000503": {"bank": "Wells Fargo Bank", "city": "Philadelphia", "state": "PA", "type": "ABA"},
    "031100209": {"bank": "PNC Bank", "city": "Philadelphia", "state": "PA", "type": "ABA"},
    "031201360": {"bank": "Citizens Bank", "city": "Philadelphia", "state": "PA", "type": "ABA"},
    "036001808": {"bank": "Barclays Bank Delaware", "city": "Wilmington", "state": "DE", "type": "ABA"},
    "041000124": {"bank": "KeyBank", "city": "Cleveland", "state": "OH", "type": "ABA"},
    "041000153": {"bank": "Huntington National Bank", "city": "Columbus", "state": "OH", "type": "ABA"},
    "042000314": {"bank": "Fifth Third Bank", "city": "Cincinnati", "state": "OH", "type": "ABA"},
    "043000096": {"bank": "PNC Bank", "city": "Pittsburgh", "state": "PA", "type": "ABA"},
    "051000017": {"bank": "Bank of America", "city": "Richmond", "state": "VA", "type": "ABA"},
    "051000020": {"bank": "First Citizens Bank", "city": "Raleigh", "state": "NC", "type": "ABA"},
    "053000219": {"bank": "Bank of America", "city": "Charlotte", "state": "NC", "type": "ABA"},
    "054001204": {"bank": "Capital One", "city": "McLean", "state": "VA", "type": "ABA"},
    "061000104": {"bank": "Bank of America", "city": "Atlanta", "state": "GA", "type": "ABA"},
    "061000227": {"bank": "SunTrust Bank (Truist)", "city": "Atlanta", "state": "GA", "type": "ABA"},
    "061092387": {"bank": "Regions Bank", "city": "Birmingham", "state": "AL", "type": "ABA"},
    "065000090": {"bank": "JPMorgan Chase Bank", "city": "Baton Rouge", "state": "LA", "type": "ABA"},
    "071000013": {"bank": "JPMorgan Chase Bank", "city": "Chicago", "state": "IL", "type": "ABA"},
    "071000505": {"bank": "Bank of America", "city": "Chicago", "state": "IL", "type": "ABA"},
    "071006486": {"bank": "BMO Harris Bank", "city": "Chicago", "state": "IL", "type": "ABA"},
    "071025661": {"bank": "Citibank", "city": "Chicago", "state": "IL", "type": "ABA"},
    "071926809": {"bank": "Discover Bank", "city": "Greenwood", "state": "DE", "type": "ABA"},
    "073000228": {"bank": "Wells Fargo Bank", "city": "Des Moines", "state": "IA", "type": "ABA"},
    "075000022": {"bank": "Associated Bank", "city": "Green Bay", "state": "WI", "type": "ABA"},
    "081000032": {"bank": "US Bank", "city": "St. Louis", "state": "MO", "type": "ABA"},
    "081000210": {"bank": "Commerce Bank", "city": "Kansas City", "state": "MO", "type": "ABA"},
    "086000011": {"bank": "US Bank", "city": "Minneapolis", "state": "MN", "type": "ABA"},
    "091000019": {"bank": "Wells Fargo Bank", "city": "Minneapolis", "state": "MN", "type": "ABA"},
    "091000022": {"bank": "US Bank", "city": "Minneapolis", "state": "MN", "type": "ABA"},
    "091300010": {"bank": "Bremer Bank", "city": "Saint Paul", "state": "MN", "type": "ABA"},
    "101000019": {"bank": "Bank of America", "city": "Dallas", "state": "TX", "type": "ABA"},
    "102000076": {"bank": "Wells Fargo Bank", "city": "Denver", "state": "CO", "type": "ABA"},
    "103000648": {"bank": "Bank of Oklahoma", "city": "Tulsa", "state": "OK", "type": "ABA"},
    "111000025": {"bank": "Bank of America", "city": "Dallas", "state": "TX", "type": "ABA"},
    "111000614": {"bank": "JPMorgan Chase Bank", "city": "Dallas", "state": "TX", "type": "ABA"},
    "111900659": {"bank": "Wells Fargo Bank", "city": "San Antonio", "state": "TX", "type": "ABA"},
    "113000023": {"bank": "Frost Bank", "city": "San Antonio", "state": "TX", "type": "ABA"},
    "113024588": {"bank": "Compass Bank (BBVA)", "city": "Birmingham", "state": "AL", "type": "ABA"},
    "121000248": {"bank": "Wells Fargo Bank", "city": "San Francisco", "state": "CA", "type": "ABA"},
    "121042882": {"bank": "Wells Fargo Bank", "city": "Sacramento", "state": "CA", "type": "ABA"},
    "121100782": {"bank": "Bank of the West", "city": "San Francisco", "state": "CA", "type": "ABA"},
    "121137522": {"bank": "Charles Schwab Bank", "city": "Reno", "state": "NV", "type": "ABA"},
    "121301015": {"bank": "Bank of America", "city": "San Francisco", "state": "CA", "type": "ABA"},
    "122000247": {"bank": "Wells Fargo Bank", "city": "Los Angeles", "state": "CA", "type": "ABA"},
    "122016066": {"bank": "JPMorgan Chase Bank", "city": "Los Angeles", "state": "CA", "type": "ABA"},
    "122105155": {"bank": "Citibank", "city": "Las Vegas", "state": "NV", "type": "ABA"},
    "123006800": {"bank": "US Bank", "city": "Portland", "state": "OR", "type": "ABA"},
    "124000054": {"bank": "Zions Bank", "city": "Salt Lake City", "state": "UT", "type": "ABA"},
    "124303201": {"bank": "America First Credit Union", "city": "Riverdale", "state": "UT", "type": "ABA"},
    "125000024": {"bank": "Bank of America", "city": "Seattle", "state": "WA", "type": "ABA"},
    "125008547": {"bank": "Washington Federal Bank", "city": "Seattle", "state": "WA", "type": "ABA"},
    "125200057": {"bank": "JPMorgan Chase Bank", "city": "Seattle", "state": "WA", "type": "ABA"},
    "231372691": {"bank": "Ally Bank", "city": "Sandy", "state": "UT", "type": "ABA"},
    "241070417": {"bank": "Ally Bank", "city": "Detroit", "state": "MI", "type": "ABA"},
    "267084131": {"bank": "Navy Federal Credit Union", "city": "Vienna", "state": "VA", "type": "ABA"},
    "272471548": {"bank": "Alliant Credit Union", "city": "Chicago", "state": "IL", "type": "ABA"},
    "291380528": {"bank": "Marcus by Goldman Sachs", "city": "Salt Lake City", "state": "UT", "type": "ABA"},
    "314074269": {"bank": "USAA Federal Savings Bank", "city": "San Antonio", "state": "TX", "type": "ABA"},
    "322271627": {"bank": "JPMorgan Chase Bank", "city": "Columbus", "state": "OH", "type": "ABA"},
    "325070760": {"bank": "Bank of America", "city": "Seattle", "state": "WA", "type": "ABA"},
}

def _checksum(routing: str) -> bool:
    if len(routing) != 9 or not routing.isdigit():
        return False
    d = [int(c) for c in routing]
    total = (3*(d[0]+d[3]+d[6]) + 7*(d[1]+d[4]+d[7]) + 1*(d[2]+d[5]+d[8]))
    return total % 10 == 0

def lookup_routing(routing_number: str) -> dict:
    rn = routing_number.strip().replace("-", "").replace(" ", "")

    if not rn.isdigit():
        return {"status": "error", "error": "Routing number must contain only digits"}
    if len(rn) != 9:
        return {"status": "error", "error": f"Routing number must be exactly 9 digits, got {len(rn)}"}

    checksum_valid = _checksum(rn)

    if not checksum_valid:
        return {
            "status": "invalid",
            "routing_number": rn,
            "valid": False,
            "checksum": False,
            "error": "Failed ABA checksum validation"
        }

    if rn in ROUTING_NUMBERS:
        data = ROUTING_NUMBERS[rn]
        return {
            "status": "success",
            "routing_number": rn,
            "valid": True,
            "checksum": True,
            "bank_name": data["bank"],
            "city": data["city"],
            "state": data["state"],
            "type": data["type"]
        }

    return {
        "status": "valid_unknown",
        "routing_number": rn,
        "valid": True,
        "checksum": True,
        "bank_name": "Unknown - not in database",
        "note": "Checksum passed but bank not in local database"
    }
