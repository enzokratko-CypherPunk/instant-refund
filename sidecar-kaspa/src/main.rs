use axum::{routing::get, Json, Router, response::IntoResponse};
use serde_json::json;
use tokio::net::TcpListener;

use secp256k1::{Secp256k1, SecretKey, PublicKey};

fn env_default(key: &str, default: &str) -> String {
    std::env::var(key).unwrap_or_else(|_| default.to_string())
}

fn require_mainnet() -> Result<(), String> {
    let net = env_default("KASPA_NETWORK", "mainnet");
    if net.to_lowercase() != "mainnet" {
        return Err(format!("KASPA_NETWORK must be 'mainnet' (got: {})", net));
    }
    Ok(())
}

// Parse 32-byte hex WITHOUT external crates
fn decode_hex_32(s: &str) -> Result<[u8; 32], String> {
    let s = s.trim().trim_start_matches("0x");
    if s.len() != 64 {
        return Err(format!("private key must be 64 hex chars (got {})", s.len()));
    }

    let mut out = [0u8; 32];
    for i in 0..32 {
        let byte_str = &s[i*2..i*2+2];
        out[i] = u8::from_str_radix(byte_str, 16)
            .map_err(|_| format!("invalid hex at byte {}", i))?;
    }
    Ok(out)
}

fn derive_wallet_id() -> Result<String, String> {
    let pk_hex = std::env::var("KASPA_SIGNER_PRIVATE_KEY")
        .map_err(|_| "missing env var KASPA_SIGNER_PRIVATE_KEY".to_string())?;

    let bytes = decode_hex_32(&pk_hex)?;

    let sk = SecretKey::from_slice(&bytes)
        .map_err(|_| "invalid secp256k1 private key".to_string())?;

    let secp = Secp256k1::new();
    let pk = PublicKey::from_secret_key(&secp, &sk);

    // Stable, dependency-free identifier
    Ok(format!("{:?}", pk.serialize()))
}

async fn healthz() -> impl IntoResponse {
    Json(json!({ "status": "ok" }))
}

async fn debug_wallet() -> impl IntoResponse {
    let network = env_default("KASPA_NETWORK", "mainnet");

    if let Err(e) = require_mainnet() {
        return Json(json!({
            "network": network,
            "wallet_id": "UNRESOLVED",
            "balance": 0,
            "utxos": [],
            "error": e
        }));
    }

    match derive_wallet_id() {
        Ok(wallet_id) => Json(json!({
            "network": "mainnet",
            "wallet_id": wallet_id,
            "balance": 0,
            "utxos": [],
            "note": "Layer 3.1 stable. Next: derive Kaspa address + UTXO discovery."
        })),
        Err(e) => Json(json!({
            "network": "mainnet",
            "wallet_id": "UNRESOLVED",
            "balance": 0,
            "utxos": [],
            "error": e
        }))
    }
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/healthz", get(healthz))
        .route("/debug/wallet", get(debug_wallet));

    let port = env_default("SIDECAR_HTTP_PORT", "8080");
    let addr = format!("0.0.0.0:{}", port);

    let listener = TcpListener::bind(&addr)
        .await
        .expect("failed to bind listener");

    println!("Sidecar listening on {}", addr);

    axum::serve(listener, app)
        .await
        .expect("server error");
}
