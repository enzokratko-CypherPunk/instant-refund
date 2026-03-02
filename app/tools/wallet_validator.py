from typing import Dict, Any
import re

CHAIN_PATTERNS: Dict[str, Dict] = {
    "Bitcoin": {"pattern": r"^(1|3)[a-km-zA-HJ-NP-Z1-9]{25,34}$|^bc1[a-z0-9]{39,59}$", "symbol": "BTC"},
    "Ethereum": {"pattern": r"^0x[a-fA-F0-9]{40}$", "symbol": "ETH"},
    "Litecoin": {"pattern": r"^[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}$|^ltc1[a-z0-9]{39,59}$", "symbol": "LTC"},
    "Ripple": {"pattern": r"^r[0-9a-zA-Z]{24,34}$", "symbol": "XRP"},
    "Solana": {"pattern": r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", "symbol": "SOL"},
    "Cardano": {"pattern": r"^addr1[a-z0-9]{50,100}$", "symbol": "ADA"},
    "Dogecoin": {"pattern": r"^D[5-9A-HJ-NP-U][1-9A-HJ-NP-Za-km-z]{32}$", "symbol": "DOGE"},
    "Polkadot": {"pattern": r"^1[a-zA-Z0-9]{46,47}$", "symbol": "DOT"},
    "Avalanche": {"pattern": r"^0x[a-fA-F0-9]{40}$|^X-avax[a-zA-Z0-9]{39}$", "symbol": "AVAX"},
    "Tron": {"pattern": r"^T[a-zA-Z0-9]{33}$", "symbol": "TRX"},
    "Kaspa": {"pattern": r"^kaspa:[a-z0-9]{61,63}$", "symbol": "KAS"},
    "Binance": {"pattern": r"^0x[a-fA-F0-9]{40}$|^bnb[a-z0-9]{39}$", "symbol": "BNB"},
    "Polygon": {"pattern": r"^0x[a-fA-F0-9]{40}$", "symbol": "MATIC"},
    "Cosmos": {"pattern": r"^cosmos[a-z0-9]{39}$", "symbol": "ATOM"},
    "Algorand": {"pattern": r"^[A-Z2-7]{58}$", "symbol": "ALGO"},
    "Stellar": {"pattern": r"^G[A-Z2-7]{55}$", "symbol": "XLM"},
    "Monero": {"pattern": r"^4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}$", "symbol": "XMR"},
    "Chainlink": {"pattern": r"^0x[a-fA-F0-9]{40}$", "symbol": "LINK"},
    "VeChain": {"pattern": r"^0x[a-fA-F0-9]{40}$", "symbol": "VET"},
    "Filecoin": {"pattern": r"^f[0-4][a-zA-Z0-9]{5,100}$", "symbol": "FIL"},
}

def validate_wallet(address: str, chain: str = "") -> Dict[str, Any]:
    clean = address.strip()

    if not clean:
        return {"status": "error", "error": "Address is required"}

    if chain:
        chain_title = chain.strip().title()
        if chain_title in CHAIN_PATTERNS:
            data = CHAIN_PATTERNS[chain_title]
            valid = bool(re.match(data["pattern"], clean))
            return {
                "status": "success",
                "address": clean,
                "chain": chain_title,
                "symbol": data["symbol"],
                "valid": valid,
                "error": None if valid else f"Address format invalid for {chain_title}"
            }
        return {"status": "error", "error": f"Unknown chain: {chain}"}

    matches = []
    for chain_name, data in CHAIN_PATTERNS.items():
        if re.match(data["pattern"], clean):
            matches.append({"chain": chain_name, "symbol": data["symbol"]})

    if matches:
        return {
            "status": "success",
            "address": clean,
            "valid": True,
            "possible_chains": matches,
            "chain_count": len(matches)
        }

    return {
        "status": "not_found",
        "address": clean,
        "valid": False,
        "possible_chains": [],
        "error": "Address does not match any known chain format"
    }
