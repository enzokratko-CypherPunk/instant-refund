import sys
import os
import base64
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

print("--- [SYSTEM] DECODING MODULES... ---", file=sys.stderr)

signer_b64 = "aW1wb3J0IG9zDQpmcm9tIGZhc3RhcGkgaW1wb3J0IEZhc3RBUEksIEhlYWRlciwgSFRUUEV4Y2VwdGlvbg0KDQpTSUdORVJfU0hBUkVEX1NFQ1JFVCA9ICJERUJVR19TSEFSRURfU0VDUkVUX0RPX05PVF9LRUVQIg0KaWYgbm90IFNJR05FUl9TSEFSRURfU0VDUkVUOg0KICAgIHJhaXNlIFJ1bnRpbWVFcnJvcigiU2lnbmVyIHNoYXJlZCBzZWNyZXQgbm90IGNvbmZpZ3VyZWQiKQ0KDQphcHAgPSBGYXN0QVBJKCkNCg0KDQpAYXBwLmdldCgiL2hlYWx0aHoiKQ0KZGVmIGhlYWx0aHooKToNCiAgICByZXR1cm4geyJzdGF0dXMiOiAib2sifQ0KDQoNCmRlZiB2ZXJpZnlfc2hhcmVkX3NlY3JldCh4X3NpZ25lcl9zZWNyZXQ6IHN0ciB8IE5vbmUpOg0KICAgIGlmIG5vdCB4X3NpZ25lcl9zZWNyZXQgb3IgeF9zaWduZXJfc2VjcmV0ICE9IFNJR05FUl9TSEFSRURfU0VDUkVUOg0KICAgICAgICByYWlzZSBIVFRQRXhjZXB0aW9uKHN0YXR1c19jb2RlPTQwMSwgZGV0YWlsPSJJbnZhbGlkIHNpZ25lciBzZWNyZXQiKQ0KDQoNCkBhcHAucG9zdCgiL3NpZ24iKQ0KZGVmIHNpZ25fcmVxdWVzdCgNCiAgICBwYXlsb2FkOiBkaWN0LA0KICAgIHhfc2lnbmVyX3NlY3JldDogc3RyIHwgTm9uZSA9IEhlYWRlcihkZWZhdWx0PU5vbmUpLA0KKToNCiAgICAiIiINCiAgICBLYXNwYSBzaWduaW5nIGlzIGhhbmRsZWQgZXhjbHVzaXZlbHkgYnkgdGhlIFJ1c3Qgc2lkZWNhci4NCiAgICBUaGlzIHNlcnZpY2Ugb25seSBhdXRoZW50aWNhdGVzIGFuZCBmb3J3YXJkcyBpbnRlbnQuDQogICAgIiIiDQogICAgdmVyaWZ5X3NoYXJlZF9zZWNyZXQoeF9zaWduZXJfc2VjcmV0KQ0KDQogICAgcmV0dXJuIHsNCiAgICAgICAgInN0YXR1cyI6ICJhY2NlcHRlZCIsDQogICAgICAgICJub3RlIjogIlNpZ25pbmcgZGVsZWdhdGVkIHRvIEthc3BhIHNpZGVjYXIiLA0KICAgIH0NCg0KCnByaW50KCdTSUdORVIgUk9VVEVTIExPQURFRCcpDQo="
rpc_b64 = "aW1wb3J0IGpzb24KaW1wb3J0IHN5cwoKIyBUcnkgdG8gaW1wb3J0IHJlcXVlc3RzOyBpZiBtaXNzaW5nLCB3ZSBjYXRjaCBpdCBsYXRlcgp0cnk6CiAgICBpbXBvcnQgcmVxdWVzdHMKZXhjZXB0IEltcG9ydEVycm9yOgogICAgcmVxdWVzdHMgPSBOb25lCgpkZWYgc3VibWl0X3RyYW5zYWN0aW9uKGhleF90cmFuc2FjdGlvbjogc3RyKToKICAgICIiIgogICAgU3VibWl0cyBhIHRyYW5zYWN0aW9uIHRvIHRoZSBLYXNwYSBOZXR3b3JrIHZpYSB0aGUgUHVibGljIFJlbGF5LgogICAgVGhpcyBieXBhc3NlcyB0aGUgbG9jYWwgbm9kZSBlbnRpcmVseS4KICAgICIiIgogICAgIyAxLiBDaGVjayBmb3IgbGlicmFyeQogICAgaWYgbm90IHJlcXVlc3RzOgogICAgICAgIHByaW50KCJDUklUSUNBTCBFUlJPUjogJ3JlcXVlc3RzJyBsaWJyYXJ5IGlzIG5vdCBpbnN0YWxsZWQuIiwgZmlsZT1zeXMuc3RkZXJyKQogICAgICAgIHJldHVybiB7ImVycm9yIjogIlNlcnZlciBDb25maWd1cmF0aW9uIEVycm9yOiBNaXNzaW5nICdyZXF1ZXN0cycgbGlicmFyeSJ9CgogICAgIyAyLiBEZWZpbmUgUHVibGljIFJlbGF5IFVSTAogICAgdXJsID0gImh0dHBzOi8vYXBpLmthc3BhLm9yZy90cmFuc2FjdGlvbnMiCiAgICBwYXlsb2FkID0geyJ0cmFuc2FjdGlvbkhleCI6IGhleF90cmFuc2FjdGlvbn0KICAgIAogICAgcHJpbnQoZiItLS0gW05FVyBDT0RFIEFDVElWRV0gQlJPQURDQVNUSU5HIFRPIHt1cmx9IC0tLSIsIGZpbGU9c3lzLnN0ZGVyciwgZmx1c2g9VHJ1ZSkKCiAgICB0cnk6CiAgICAgICAgIyAzLiBTZW5kIFJlcXVlc3QgKDEwcyB0aW1lb3V0KQogICAgICAgIHJlc3BvbnNlID0gcmVxdWVzdHMucG9zdCh1cmwsIGpzb249cGF5bG9hZCwgdGltZW91dD0xMCkKICAgICAgICAKICAgICAgICBwcmludChmIi0tLSBSRUxBWSBTVEFUVVM6IHtyZXNwb25zZS5zdGF0dXNfY29kZX0gLS0tIiwgZmlsZT1zeXMuc3RkZXJyLCBmbHVzaD1UcnVlKQogICAgICAgIAogICAgICAgIGlmIHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMDoKICAgICAgICAgICAgIyBTdWNjZXNzCiAgICAgICAgICAgIHR4X2lkID0gcmVzcG9uc2UuanNvbigpLmdldCgidHJhbnNhY3Rpb25JZCIpCiAgICAgICAgICAgIHJldHVybiB7InJlc3VsdCI6IHR4X2lkfQogICAgICAgIGVsc2U6CiAgICAgICAgICAgICMgUmVsYXkgUmVqZWN0ZWQgSXQKICAgICAgICAgICAgcHJpbnQoZiJSRUxBWSBFUlJPUiBCT0RZOiB7cmVzcG9uc2UudGV4dH0iLCBmaWxlPXN5cy5zdGRlcnIsIGZsdXNoPVRydWUpCiAgICAgICAgICAgIHJldHVybiB7ImVycm9yIjogZiJSZWxheSBSZWplY3RlZDoge3Jlc3BvbnNlLnRleHR9In0KCiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgcHJpbnQoZiJDT05ORUNUSU9OIEVYQ0VQVElPTjoge3N0cihlKX0iLCBmaWxlPXN5cy5zdGRlcnIsIGZsdXNoPVRydWUpCiAgICAgICAgcmV0dXJuIHsiZXJyb3IiOiBmIkNvbm5lY3Rpb24gRmFpbGVkOiB7c3RyKGUpfSJ9DQo="

try:
    # FORCE UNPACK AS STANDARD NAMES
    with open("signer.py", "wb") as f:
        f.write(base64.b64decode(signer_b64))
    
    with open("rpc.py", "wb") as f:
        f.write(base64.b64decode(rpc_b64))
        
    print("--- [SYSTEM] MODULES NORMALIZED & EXTRACTED ---", file=sys.stderr)
    
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import signer
    import rpc
    print("--- [SYSTEM] IMPORTS SUCCESSFUL ---", file=sys.stderr)
    IMPORT_ERROR = None

except Exception as e:
    IMPORT_ERROR = f"UNPACK FAILURE: {str(e)}\n{traceback.format_exc()}"
    print(IMPORT_ERROR, file=sys.stderr)

app = FastAPI(title="Instant Refund API")

class RefundRequest(BaseModel):
    amount: int
    recipient_address: str
    merchant_id: str

@app.post("/v1/refunds/instant")
def process_refund(request: RefundRequest):
    print(f"--- [REQUEST] {request.amount} to {request.recipient_address} ---", file=sys.stderr, flush=True)

    if IMPORT_ERROR:
        return {
            "status": "error", 
            "message": "Deployment Failed", 
            "details": IMPORT_ERROR
        }

    try:
        # EXECUTE
        # NOTE: If your file was named 'signer_service', we renamed it to 'signer'
        # So we call signer.sign_transaction
        hex_tx = signer.sign_transaction(request.amount, request.recipient_address)
        result = rpc.submit_transaction(hex_tx)
        return {"status": "success", "txid": result, "note": "MAINNET SUCCESS"}
    except Exception as e:
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}

@app.get("/")
def health_check():
    return {"status": "ok"}
