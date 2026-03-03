from typing import Dict, Any, List
import httpx
import csv
import io

OFAC_URL = "https://data.opensanctions.org/datasets/latest/us_ofac_sdn/targets.simple.csv"

_SDN_CACHE: List[Dict] = []
_CACHE_DATE: str = ""

async def _load_ofac_list() -> List[Dict]:
    global _SDN_CACHE, _CACHE_DATE
    from datetime import date
    today = str(date.today())
    if _SDN_CACHE and _CACHE_DATE == today:
        return _SDN_CACHE
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(OFAC_URL, timeout=60)
        raw = resp.content.decode("utf-8", errors="replace")
    records = []
    reader = csv.DictReader(io.StringIO(raw))
    for row in reader:
        name = row.get("name", "").strip()
        aliases = row.get("aliases", "").strip()
        sanctions = row.get("sanctions", "").strip()
        schema = row.get("schema", "").strip()
        if name:
            records.append({
                "name": name.lower(),
                "display_name": name,
                "aliases": aliases,
                "type": schema,
                "program": sanctions,
                "remarks": "",
            })
    _SDN_CACHE = records
    _CACHE_DATE = today
    return records

def _fuzzy_score(query: str, candidate: str, aliases: str = "") -> int:
    q_words = set(query.lower().split())
    c_clean = candidate.lower().replace(",", " ")
    a_clean = aliases.lower().replace(";", " ").replace(",", " ")
    combined = c_clean + " " + a_clean
    c_words = set(combined.split())
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
    contains_bonus = 15 if all(w in combined for w in q_words) else 0
    return min(100, int(f1 * 100) + contains_bonus)

async def check_sanctions(name: str, threshold: int = 60  # default) -> Dict[str, Any]:
    if not name or len(name.strip()) < 2:
        return {"status": "error", "error": "Name must be at least 2 characters"}
    records = await _load_ofac_list()
    if not records:
        return {"status": "error", "error": "Sanctions list unavailable. Please try again shortly."}
    query = name.strip().lower()
    matches = []
    for record in records:
        score = _fuzzy_score(query, record["name"], record["aliases"])
        if score >= threshold:
            matches.append({
                "matched_name": record["display_name"],
                "aliases": record["aliases"],
                "score": score,
                "type": record["type"],
                "program": record["program"],
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
        "list_source": "OFAC SDN via OpenSanctions"
    }

async def get_sanctions_status() -> Dict[str, Any]:
    from datetime import date
    records = await _load_ofac_list()
    return {
        "status": "success",
        "list": "OFAC SDN",
        "source": "US Treasury via OpenSanctions",
        "url": OFAC_URL,
        "records_loaded": len(records),
        "cache_date": str(date.today()),
        "update_frequency": "Daily"
    }


