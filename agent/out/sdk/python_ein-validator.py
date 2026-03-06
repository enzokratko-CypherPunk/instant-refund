import requests

BASE = "https://instant-refund-api-l99qr.ondigitalocean.app"
url = BASE + "/v1/tools/ein/{ein}"

r = requests.request("GET", url, timeout=30)
print(r.status_code)
print(r.json())
