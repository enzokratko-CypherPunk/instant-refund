from typing import Dict, Any, List
import httpx
import csv
import io

OFAC_URL = "https://ofac.treasury.gov/downloads/sdn.csv"

_SDN_CACHE: List[Dict] = []
_CACHE_DATE: str = ""

async def _load_ofac_list() -> List[Dict]:
    global _SDN_CACHE, _CACHE_DATE
    from datetime import date
    today = str(date.today())
    if _SDN_CACHE and _CACHE_DATE == today:
        return _SDN_CACHE
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/csv,text/plain,*/*",
        "Accept-Encoding": "identity"
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(OFAC_URL, timeout=30, headers=headers)
        content = resp.content.decode("latin-1", errors="replace")
    records = []
    reader = csv.reader(io.StringIO(content))
    for row in reader:
        if len(row) >= 4 and row[1].strip() and row[1].strip() != "SDN_Name":
            records.append({
                "name": row[1].strip().lower(),
                "display_name": row[1].strip(),
                "type": row[2].strip() if len(row) > 2 else "",
                "program": row[3].strip() if len(row) > 3 else "",
                "remarks": row[11].strip() if len(row) > 11 else "",
            })
    _SDN_CACHE = records
    _CACHE_DATE = today
    return records

def _fuzzy_score(query: str, candidate: str) -> int:
    q_words = set(query.lower().split())
    c_clean = candidate.lower().replace(",", " ")
    c_words = set(c_clean.split())
    if not q_words or not c_words:
        return 0
    intersection = q_words & c_words
    if not intersection:
        return 0
    precision = len(intersection) / len(q_words)
    recall = len(intersection) / len(c_words)
    if precision + recall == 0:
        return 0
    f1 = 2 * precision * recall / (precision + recall)
    contains_bonus = 15 if all(w in c_clean for w in q_words) else 0
    return min(100, int(f1 * 100) + contains_bonus)

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
