from app.tools.payment_intelligence import analyze_payment
from app.tools.defi_health import check_defi_health
from app.tools.ein_validator import validate_ein
from app.tools.token_price import get_token_price
from app.tools.fraud_score import calculate_fraud_score
from app.tools.iso8583_parser import parse_iso8583
from app.tools.routing_validator import lookup_routing
from app.tools.pep_checker import check_pep, get_pep_status
# Sanctions threshold: 60
from app.tools.sanctions_checker import check_sanctions, get_sanctions_status
from app.tools.wallet_validator import validate_wallet
from app.tools.currency_converter import convert_currency
from app.tools.swift_lookup import lookup_swift
from app.tools.decline_codes import interpret_decline_code
from app.tools.iban_validator import validate_iban

from app.tools.bin_lookup import get_bin_details
from app.tools.mcc_lookup import get_mcc_details
"""
Instant Refund API entrypoint (DigitalOcean App Platform).

This module is the authoritative router wiring point.
"""

import os
import socket
import time
import base64
import hmac
import hashlib
import httpx

from app.api import app
from app.routes.refunds import router as refunds_router


# ---- Core router wiring (DETERMINISTIC) ----
app.include_router(refunds_router)


# ---- Debug endpoints ----

@app.get("/debug/kaspad-connect")
def debug_kaspad_connect():
    host = os.getenv("KASPA_RPC_HOST", "10.17.0.5")
    port = int(os.getenv("KASPA_RPC_PORT", "16110"))
    timeout = float(os.getenv("KASPA_RPC_TIMEOUT", "3"))

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return {"status": "ok", "message": f"Connected to kaspad at {host}:{port}"}
    except Exception as e:
        return {"status": "error", "error": str(e), "target": f"{host}:{port}"}


@app.get("/__debug/signer-test")
async def debug_signer_test():
    secret_b64 = os.getenv("SIGNER_SHARED_SECRET")
    if not secret_b64:
        return {"error": "SIGNER_SHARED_SECRET not set"}

    shared_secret = base64.b64decode(secret_b64)

    payload = "hello-signer"
    timestamp = int(time.time())

    msg = f"{payload}:{timestamp}".encode()
    sig = hmac.new(shared_secret, msg, hashlib.sha256).digest()
    sig_b64 = base64.b64encode(sig).decode()

    body = {
        "payload": payload,
        "timestamp": timestamp,
        "signature": sig_b64
    }

    signer_url = "https://instant-refund-api-l99qr.ondigitalocean.app/signer/sign"

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(signer_url, json=body)

    if resp.status_code != 200:
        return {"error": resp.text}

    return resp.json()
# --- Day 1: BIN Lookup Tool ---
@app.get("/v1/tools/bin/{bin_code}")
async def bin_tool(bin_code: str):
    return get_bin_details(bin_code)

# --- Day 2: MCC Lookup Tool ---
@app.get("/v1/tools/mcc/{mcc_code}")
async def mcc_tool(mcc_code: str):
    return get_mcc_details(mcc_code)

# --- Tool 3: IBAN Validator ---
@app.get("/v1/tools/iban/{iban_code}")
async def iban_tool(iban_code: str):
    return validate_iban(iban_code)


# --- Tool 4: Decline Code Interpreter ---
@app.get("/v1/tools/decline/{code}")
async def decline_tool(code: str):
    return interpret_decline_code(code)


# --- Tool 5: SWIFT/BIC Lookup ---
@app.get("/v1/tools/swift/{swift_code}")
async def swift_tool(swift_code: str):
    return lookup_swift(swift_code)


# --- Tool 6: Currency Converter ---
@app.get("/v1/tools/currency/{from_currency}/{to_currency}/{amount}")
async def currency_tool(from_currency: str, to_currency: str, amount: float):
    return await convert_currency(from_currency, to_currency, amount)


# --- Tool 7: Wallet Address Validator ---
@app.get("/v1/tools/wallet/{address}")
async def wallet_tool(address: str, chain: str = ""):
    return validate_wallet(address, chain)


# --- Tool 8: Sanctions List Checker ---
@app.get("/v1/tools/sanctions/status")
async def sanctions_status():
    return await get_sanctions_status()

@app.get("/v1/tools/sanctions/screen/{name}")
async def sanctions_screen(name: str, threshold: int = 60):
    return await check_sanctions(name, threshold)



# --- Tool 9: PEP Screening ---
@app.get("/v1/tools/pep/status")
async def pep_status():
    return await get_pep_status()

@app.get("/v1/tools/pep/screen/{name}")
async def pep_screen(name: str, threshold: int = 60):
    return await check_pep(name, threshold)

# --- Tool 10: Routing Number Validator ---
@app.get("/v1/tools/routing/{routing_number}")
async def routing_tool(routing_number: str):
    return lookup_routing(routing_number)


# --- Tool 11: ISO 8583 Message Parser ---
@app.get("/v1/tools/iso8583/{message}")
async def iso8583_tool(message: str):
    return parse_iso8583(message)


# --- Tool 12: Card BIN Fraud Score ---
@app.get("/v1/tools/fraud-score")
async def fraud_score_tool(
    card_type: str = "credit",
    network: str = "Visa",
    country_code: str = "US",
    is_commercial: bool = False,
    is_anonymous: bool = False
):
    return calculate_fraud_score(card_type, network, country_code, is_commercial, is_anonymous)

# --- Tool 13: Token Price Feed ---
@app.get("/v1/tools/token-price/{token}")
async def token_price_tool(token: str, currency: str = "usd"):
    return await get_token_price(token, currency)

# --- Tool 14: EIN / Business Registry Verifier ---
@app.get("/v1/tools/ein/{ein}")
async def ein_validator_tool(ein: str):
    return validate_ein(ein)

# --- Tool 15: DeFi Health Checker ---
@app.get("/v1/tools/defi-health/{protocol}")
async def defi_health_tool(protocol: str):
    return await check_defi_health(protocol)

# --- Tool 16: Payment Intelligence API (Flagship) ---
@app.get("/v1/tools/payment-intelligence")
async def payment_intelligence_tool(
    card_bin: str = "411111",
    decline_code: str = "51",
    merchant_mcc: str = "5411",
    transaction_amount: float = 100.00,
    country_code: str = "US",
    card_type: str = "credit",
    network: str = "Visa"
):
    return await analyze_payment(card_bin, decline_code, merchant_mcc, transaction_amount, country_code, card_type, network)

