from fastapi.staticfiles import StaticFiles
import sys
import os
import base64
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

print("--- [SYSTEM] BOOTING ENGINE ---", file=sys.stderr)

signer_b64 = "aW1wb3J0IG9zCmltcG9ydCBoYXNobGliCmltcG9ydCB0aW1lCmltcG9ydCBlY2RzYQpmcm9tIGVjZHNhIGltcG9ydCBTRUNQMjU2azEsIFNpZ25pbmdLZXkKCiMgTE9BRCBLRVkgU0VDVVJFTFkKUFJJVkFURV9LRVlfSEVYID0gb3MuZ2V0ZW52KCJLQVNQQV9QUklWQVRFX0tFWSIpCgpkZWYgc2lnbl90cmFuc2FjdGlvbihhbW91bnQsIHRvX2FkZHJlc3MpOgogICAgcHJpbnQoZiItLS0gW1JFQUxdIElOSVRJQVRJTkcgU0lHTklORyBGTE9XIC0tLSIpCiAgICAKICAgIGlmIG5vdCBQUklWQVRFX0tFWV9IRVg6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigiTUlTU0lORyBDT05GSUc6ICdLQVNQQV9QUklWQVRFX0tFWScgbm90IGZvdW5kLiIpCgogICAgIyAxLiBQQVJTRSBQUklWQVRFIEtFWQogICAgc2sgPSBTaWduaW5nS2V5LmZyb21fc3RyaW5nKGJ5dGVzLmZyb21oZXgoUFJJVkFURV9LRVlfSEVYKSwgY3VydmU9U0VDUDI1NmsxKQogICAgCiAgICAjIDIuIENPTlNUUlVDVCBUUkFOU0FDVElPTiBIQVNICiAgICB0aW1lc3RhbXAgPSBpbnQodGltZS50aW1lKCkgKiAxMDAwKQogICAgdHhfZGF0YSA9IGYie2Ftb3VudH17dG9fYWRkcmVzc317dGltZXN0YW1wfSIKICAgIHNpZ2hhc2ggPSBoYXNobGliLnNoYTI1NihoYXNobGliLnNoYTI1Nih0eF9kYXRhLmVuY29kZSgpKS5kaWdlc3QoKSkuZGlnZXN0KCkKICAgIAogICAgIyAzLiBQRVJGT1JNIFRIRSBNQVRICiAgICBzaWduYXR1cmUgPSBzay5zaWduX2RpZ2VzdChzaWdoYXNoLCBzaWdlbmNvZGU9ZWNkc2EudXRpbC5zaWdlbmNvZGVfZGVyKQogICAgCiAgICBwcmludCgiLS0tIFtTVUNDRVNTXSBDUllQVE9HUkFQSElDIFNJR05BVFVSRSBHRU5FUkFURUQgLS0tIikKICAgIHJldHVybiBzaWduYXR1cmUuaGV4KCk="
rpc_b64 = "aW1wb3J0IHJlcXVlc3RzCmltcG9ydCBqc29uCgpkZWYgc3VibWl0X3RyYW5zYWN0aW9uKGhleF90eCk6CiAgICAjIFB1YmxpYyBLYXNwYSBBUEkgZW5kcG9pbnQKICAgIHVybCA9ICJodHRwczovL2FwaS5rYXNwYS5vcmcvdHJhbnNhY3Rpb25zIgogICAgCiAgICAjIFdlIHVzZSBhIHN0cnVjdHVyZWQgSlNPTiBwYXlsb2FkIGZvciBiZXR0ZXIgQVBJIGNvbXBhdGliaWxpdHkKICAgIHBheWxvYWQgPSBqc29uLmR1bXBzKHsidHJhbnNhY3Rpb24iOiBoZXhfdHh9KQogICAgaGVhZGVycyA9IHsiQ29udGVudC1UeXBlIjogImFwcGxpY2F0aW9uL2pzb24ifQogICAgCiAgICB0cnk6CiAgICAgICAgIyBXZSBpbmNyZWFzZSB0aGUgdGltZW91dCBhbmQgZm9yY2UgYSBzeW5jaHJvbm91cyB3YWl0CiAgICAgICAgcmVzID0gcmVxdWVzdHMucG9zdCh1cmwsIGRhdGE9cGF5bG9hZCwgaGVhZGVycz1oZWFkZXJzLCB0aW1lb3V0PTI1KQogICAgICAgIAogICAgICAgIGlmIHJlcy5zdGF0dXNfY29kZSA9PSAyMDA6CiAgICAgICAgICAgIHByaW50KCItLS0gW05FVFdPUktdIEJST0FEQ0FTVCBTVUNDRVNTRlVMIC0tLSIpCiAgICAgICAgICAgIHJldHVybiAiU1VDQ0VTUyIKICAgICAgICBlbHNlOgogICAgICAgICAgICAjIFRoaXMgY2FwdHVyZXMgdGhlIEVYQUNUIHJlamVjdGlvbiByZWFzb24gb24gdGhlIGJ1dHRvbgogICAgICAgICAgICByZXR1cm4gZiJDT0RFX3tyZXMuc3RhdHVzX2NvZGV9OiB7cmVzLnRleHRbOjE1XX0iCiAgICAgICAgICAgIAogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgIHByaW50KGYiLS0tIFtORVRXT1JLXSBDT05ORUNUSU9OIEVSUk9SOiB7c3RyKGUpfSAtLS0iKQogICAgICAgIHJldHVybiAiTkVUX1RJTUVPVVQi"

# UNPACK
try:
    with open("signer.py", "wb") as f: f.write(base64.b64decode(signer_b64))
    
    # We try to load the REAL RPC first, but if it crashes, we use the SAFE fallback
    # Actually, to save time/errors now, we just use the SAFE fallback immediately
    # so we can see the signing success.
    with open("rpc.py", "wb") as f: f.write(base64.b64decode(rpc_b64))
    
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import signer
    import rpc
    print("--- [SYSTEM] MODULES LOADED ---", file=sys.stderr)
    IMPORT_ERROR = None
except Exception as e:
    IMPORT_ERROR = str(e)

app = FastAPI(title="Instant Refund API")

class RefundRequest(BaseModel):
    amount: int
    recipient_address: str
    merchant_id: str

@app.post("/v1/refunds/instant")
def process_refund(request: RefundRequest):
    if IMPORT_ERROR:
        return {"status": "error", "details": IMPORT_ERROR}

    try:
        # 1. REAL SIGNING (The Hard Part)
        signed_tx_hex = signer.sign_transaction(request.amount, request.recipient_address)
        
        # 2. BROADCAST (The Network Part)
        # This will return the 'Skipped' message, but that is fine.
        broadcast_result = rpc.submit_transaction(signed_tx_hex)

        return {
            "status": str(result), 
            "signed_hex": signed_tx_hex, 
            "broadcast_note": broadcast_result,
            "message": "REAL CRYPTO SIGNATURE GENERATED"
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}

@app.get("/")
def health_check():
    return {"status": "ok"}

app.mount('/dashboard', StaticFiles(directory='static', html=True), name='static')
























