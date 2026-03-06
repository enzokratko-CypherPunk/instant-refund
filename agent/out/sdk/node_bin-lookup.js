const BASE = "https://instant-refund-api-l99qr.ondigitalocean.app";
let url = BASE + "/v1/tools/bin/{bin_code}";

fetch(url, { method: "GET" })
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
