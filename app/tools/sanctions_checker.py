from typing import Dict, Any, List
import httpx
import csv
import io

OFAC_URL = "https://www.treasury.gov/ofac/downloads/sdn.csv"

_SDN_CACHE: List[Dict] = []
_CACHE_DATE: str = ""

async def _load_ofac_list() -> List[Dict]:
    global _SDN_CACHE, _CACHE_DATE
    from datetime import date
    today = str(date.today())
    if _SDN_CACHE and _CACHE_DATE == today:
        return _SDN_CACHE
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        resp = await client.get(OFAC_URL)
        content = resp.text
    reader = csv.reader(io.StringIO(content), quotechar='"', skipinitialspace=True)
    records = []
    for row in reader:
        if len(row) >= 12 and row[1].strip() and row[1].strip() != "-0-":
            records.append({
                "name": row[1].strip().lower(),
                "display_name": row[1].strip(),
                "type": row[2].strip() if row[2].strip() != "-0-" else "",
                "program": row[3].strip() if row[3].strip() != "-0-" else "",
                "remarks": row[11].strip() if row[11].strip() != "-0-" else "",
            })
    _SDN_CACHE = records
    _CACHE_DATE = today
    return records

def _fuzzy_score(query: str, candidate: str) -> int:
    q = set(query.lower().split())
    c = set(candidate.lower().split())
    if not q or not c:
        return 0
    intersection = q & c
    union = q | c
    jaccard = len(intersection) / len(union)
    contains_bonus = 20 if query.lower() in candidate.lower() or candidate.lower() in query.lower() else 0
    return min(100, int(jaccard * 100) + contains_bonus)

async def check_sanctions(name: str, threshold: int = 75) -> Dict[str, Any]:
    if not name or len(name.strip()) < 2:
        return {"status": "error", "error": "Name must be at least 2 characters"}

    records = await _load_ofac_list()
    query = name.strip().lower()
    matches = []

    for record in records:
        score = _fuzzy_score(query, record["name"])
        if score >= threshold:
            matches.append({
                "matched_name": record["display_name"],
                "score": score,
                "type": record["type"],
                "program": record["program"],
                "remarks": record["remarks"][:200] if record["remarks"] else "",
                "list": "OFAC SDN"
            })

    matches.sort(key=lambda x: x["score"], reverse=True)
    top_matches = matches[:5]

    return {
        "status": "success",
        "query": name,
        "threshold": threshold,
        "hit": len(top_matches) > 0,
        "match_count": len(top_matches),
        "matches": top_matches,
        "list_source": "OFAC SDN (US Treasury)"
    }

async def get_sanctions_status() -> Dict[str, Any]:
    from datetime import date
    records = await _load_ofac_list()
    return {
        "status": "success",
        "list": "OFAC SDN",
        "source": "US Treasury - Office of Foreign Assets Control",
        "url": OFAC_URL,
        "records_loaded": len(records),
        "cache_date": str(date.today()),
        "update_frequency": "Daily"
    }
