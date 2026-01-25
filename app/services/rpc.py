import requests
import json
from app.core.config import settings

def submit_transaction(hex_transaction: str):
    # SWITCHING TO OFFICIAL PUBLIC RELAY (Stable & Fast)
    url = "https://api.kaspa.org/transactions"
    
    # payload for REST API is different from RPC
    payload = {
        "transactionHex": hex_transaction
    }
    
    try:
        print(f"--- Broadcasting to {url} ---")
        response = requests.post(url, json=payload, timeout=10)
        
        # Check if successful
        if response.status_code == 200:
            # Success! Return in the format our app expects
            # api.kaspa.org returns: {"transactionId": "..."}
            tx_id = response.json().get("transactionId")
            return {"result": tx_id}
            
        else:
            # Failure
            return {"error": f"Relay Rejected: {response.text}"}
            
    except Exception as e:
        return {"error": f"Connection Failed: {str(e)}"}
