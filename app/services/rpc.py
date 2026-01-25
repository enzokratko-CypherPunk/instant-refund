import sys
import json
try:
    import requests
except ImportError:
    print("CRITICAL: REQUESTS LIBRARY MISSING", file=sys.stderr)

def submit_transaction(hex_transaction: str):
    # PUBLIC RELAY
    url = "https://api.kaspa.org/transactions"
    payload = {"transactionHex": hex_transaction}
    
    print(f"--- [STEP 4] BROADCASTING TO {url} ---", file=sys.stderr)
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"--- [STEP 5] RELAY RESPONSE: {response.status_code} ---", file=sys.stderr)
        
        if response.status_code == 200:
            return {"result": response.json().get("transactionId")}
        else:
            print(f"RELAY ERROR: {response.text}", file=sys.stderr)
            return {"error": f"Relay Rejected: {response.text}"}
    except Exception as e:
        print(f"RELAY EXCEPTION: {str(e)}", file=sys.stderr)
        return {"error": str(e)}
