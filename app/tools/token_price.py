import httpx
from typing import Optional

COINGECKO_BASE = "https://api.coingecko.com/api/v3"

SYMBOL_MAP = {
    "btc": "bitcoin", "eth": "ethereum", "usdt": "tether", "usdc": "usd-coin",
    "bnb": "binancecoin", "xrp": "ripple", "ada": "cardano", "sol": "solana",
    "doge": "dogecoin", "dot": "polkadot", "matic": "matic-network",
    "shib": "shiba-inu", "avax": "avalanche-2", "uni": "uniswap",
    "link": "chainlink", "ltc": "litecoin", "atom": "cosmos", "etc": "ethereum-classic",
    "xlm": "stellar", "algo": "algorand", "near": "near", "apt": "aptos",
    "arb": "arbitrum", "op": "optimism", "sui": "sui", "trx": "tron",
}

SUPPORTED_CURRENCIES = ["usd", "eur", "gbp", "jpy", "cad", "aud", "chf", "cny", "krw", "inr"]

async def get_token_price(token: str, currency: str = "usd") -> dict:
    token_clean = token.strip().lower()
    currency_clean = currency.strip().lower()

    if currency_clean not in SUPPORTED_CURRENCIES:
        return {"status": "error", "message": f"Unsupported currency. Supported: {', '.join(SUPPORTED_CURRENCIES)}"}

    coin_id = SYMBOL_MAP.get(token_clean, token_clean)

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                f"{COINGECKO_BASE}/simple/price",
                params={
                    "ids": coin_id,
                    "vs_currencies": currency_clean,
                    "include_24hr_change": "true",
                    "include_24hr_vol": "true",
                    "include_market_cap": "true",
                    "include_last_updated_at": "true",
                }
            )
        data = r.raise_for_status() r.json()
        if coin_id not in data:
            return {"status": "error", "message": f"Token '{token}' not found. Try using the full CoinGecko ID (e.g. 'bitcoin')."}

        d = data[coin_id]
        change = d.get(f"{currency_clean}_24h_change")

        return {
            "status": "success",
            "token": token.upper(),
            "coin_id": coin_id,
            "currency": currency_clean.upper(),
            "price": d.get(currency_clean),
            "price_change_24h_pct": round(change, 4) if change is not None else None,
            "market_cap": d.get(f"{currency_clean}_market_cap"),
            "volume_24h": d.get(f"{currency_clean}_24h_vol"),
            "last_updated_at": d.get("last_updated_at"),
            "data_source": "CoinGecko"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
