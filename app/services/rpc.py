import requests
import json
from app.core.config import settings

def submit_transaction(hex_transaction: str):
    url = f"http://{settings.KASPAD_ADDRESS}:{settings.KASPAD_PORT}/"
    payload = {
        "jsonrpc": "2.0",
        "method": "submitTransaction",
        "params": [{"transaction": {"hex": hex_transaction}, "allowOrphan": False}],
        "id": "ir-submit-01"
    }
    try:
        # Timeout set to 5 seconds to prevent Gateway Timeouts
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Node Connection Failed: {str(e)}"}
