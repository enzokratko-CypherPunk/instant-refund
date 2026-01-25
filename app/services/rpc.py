import sys
import json
# Try importing requests safely
try:
    import requests
except ImportError:
    print("CRITICAL ERROR: 'requests' library is missing!", file=sys.stderr)
    raise

def submit_transaction(hex_transaction: str):
    # USE OFFICIAL PUBLIC RELAY
    url = "https://api.kaspa.org/transactions"
    payload = {"transactionHex": hex_transaction}
    
    print(f"--- ATTEMPTING BROADCAST TO {url} ---", file=sys.stderr)
    
    try:
        # 10 second timeout to prevent hanging
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"RESPONSE CODE: {response.status_code}", file=sys.stderr)
        print(f"RESPONSE TEXT: {response.text}", file=sys.stderr)
        
        if response.status_code == 200:
            tx_id = response.json().get("transactionId")
            return {"result": tx_id}
        else:
            return {"error": f"Relay Rejected: {response.text}"}
            
    except Exception as e:
        print(f"EXCEPTION CAUGHT: {str(e)}", file=sys.stderr)
        return {"error": f"Connection Failed: {str(e)}"}
