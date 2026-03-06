import httpx
from typing import Dict, Any

PROTOCOLS = {
    "uniswap": {"name": "Uniswap", "slug": "uniswap", "chain": "Ethereum", "category": "DEX"},
    "aave": {"name": "Aave", "slug": "aave", "chain": "Multi-chain", "category": "Lending"},
    "compound": {"name": "Compound", "slug": "compound-finance", "chain": "Ethereum", "category": "Lending"},
    "curve": {"name": "Curve Finance", "slug": "curve-dex", "chain": "Multi-chain", "category": "DEX"},
    "makerdao": {"name": "MakerDAO", "slug": "makerdao", "chain": "Ethereum", "category": "CDP"},
    "lido": {"name": "Lido", "slug": "lido", "chain": "Ethereum", "category": "Liquid Staking"},
    "pancakeswap": {"name": "PancakeSwap", "slug": "pancakeswap", "chain": "BSC", "category": "DEX"},
    "uniswap-v3": {"name": "Uniswap V3", "slug": "uniswap-v3", "chain": "Multi-chain", "category": "DEX"},
    "balancer": {"name": "Balancer", "slug": "balancer", "chain": "Multi-chain", "category": "DEX"},
    "yearn": {"name": "Yearn Finance", "slug": "yearn-finance", "chain": "Ethereum", "category": "Yield"},
    "convex": {"name": "Convex Finance", "slug": "convex-finance", "chain": "Ethereum", "category": "Yield"},
    "gmx": {"name": "GMX", "slug": "gmx", "chain": "Arbitrum", "category": "Derivatives"},
    "dydx": {"name": "dYdX", "slug": "dydx", "chain": "Ethereum", "category": "Derivatives"},
    "synthetix": {"name": "Synthetix", "slug": "synthetix", "chain": "Ethereum", "category": "Derivatives"},
    "sushi": {"name": "SushiSwap", "slug": "sushi", "chain": "Multi-chain", "category": "DEX"},
}

def get_risk_level(tvl: float) -> Dict[str, str]:
    if tvl >= 1_000_000_000:
        return {"risk": "LOW", "assessment": "Large, established protocol with significant liquidity."}
    elif tvl >= 100_000_000:
        return {"risk": "MEDIUM", "assessment": "Mid-sized protocol. Monitor for liquidity changes."}
    elif tvl >= 10_000_000:
        return {"risk": "MEDIUM-HIGH", "assessment": "Smaller protocol. Higher smart contract and liquidity risk."}
    else:
        return {"risk": "HIGH", "assessment": "Low TVL protocol. Significant liquidity and exploit risk."}

async def check_defi_health(protocol: str) -> Dict[str, Any]:
    protocol_clean = protocol.strip().lower()
    
    if protocol_clean not in PROTOCOLS:
        supported = ", ".join(sorted(PROTOCOLS.keys()))
        return {
            "status": "error",
            "message": f"Protocol '{protocol}' not found.",
            "supported_protocols": supported
        }
    
    proto = PROTOCOLS[protocol_clean]
    
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"https://api.llama.fi/protocol/{proto['slug']}"
            )
            r.raise_for_status()
            data = r.json()
        
        tvl = data.get("currentChainTvls", {})
        total_tvl = data.get("tvl", [{}])
        
        if isinstance(total_tvl, list) and len(total_tvl) > 0:
            current_tvl = total_tvl[-1].get("totalLiquidityUSD", 0)
        else:
            current_tvl = 0

        prev_tvl = total_tvl[-2].get("totalLiquidityUSD", 0) if len(total_tvl) > 1 else current_tvl
        tvl_change_24h = ((current_tvl - prev_tvl) / prev_tvl * 100) if prev_tvl > 0 else 0

        risk = get_risk_level(current_tvl)

        status = "healthy"
        if tvl_change_24h < -20:
            status = "warning"
        if tvl_change_24h < -50:
            status = "critical"

        return {
            "status": "success",
            "protocol": proto["name"],
            "slug": proto["slug"],
            "chain": proto["chain"],
            "category": proto["category"],
            "health_status": status,
            "tvl_usd": round(current_tvl, 2),
            "tvl_formatted": str("USD ") + (f"{current_tvl/1_000_000_000:.2f}B" if current_tvl >= 1e9 else f"{current_tvl/1_000_000:.2f}M"),
            "tvl_change_24h_pct": round(tvl_change_24h, 4),
            "risk_level": risk["risk"],
            "risk_assessment": risk["assessment"],
            "data_source": "DeFiLlama"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


