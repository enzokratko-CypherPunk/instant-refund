from typing import Dict, Any, List
import csv
import os

PEP_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "app", "data", "peps.csv")

_PEP_CACHE: List[Dict] = []

def _load_pep_list() -> List[Dict]:
    global _PEP_CACHE
    if _PEP_CACHE:
        return _PEP_CACHE
    records = []
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "peps.csv"))
    with open(filepath, encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            if name:
                records.append({
                    "name": name.lower(),
                    "display_name": name,
                    "aliases": row.get("aliases", ""),
                    "positions": row.get("position", ""),
                    "countries": row.get("countries", ""),
                })
    _PEP_CACHE = records
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

async def check_pep(name: str, threshold: int = 60):
    if not name or len(name.strip()) < 2:
        return {"status": "error", "error": "Name must be at least 2 characters"}
    records = _load_pep_list()
    if not records:
        return {"status": "error", "error": "PEP list unavailable"}
    query = name.strip().lower()
    matches = []
    for record in records:
        score = _fuzzy_score(query, record["name"], record["aliases"])
        if score >= threshold:
            matches.append({
                "matched_name": record["display_name"],
                "aliases": record["aliases"],
                "score": score,
                "positions": record["positions"],
                "countries": record["countries"],
                "list": "PEP"
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
        "list_source": "PEP List via OpenSanctions"
    }

async def get_pep_status():
    records = _load_pep_list()
    return {
        "status": "success",
        "list": "PEP",
        "source": "OpenSanctions",
        "records_loaded": len(records),
        "update_frequency": "Daily"
    }
