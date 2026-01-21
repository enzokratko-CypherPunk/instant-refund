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

// Deterministic wallet identity from the private key.
// This is NOT a second wallet, not a new address, and not spending.
// It is simply proof the sidecar is bound to a real key.
fn derive_wallet_id() -> Result<String, String> {
    let pk_hex = std::env::var("KASPA_SIGNER_PRIVATE_KEY")
        .map_err(|_| "missing env var KASPA_SIGNER_PRIVATE_KEY".to_string())?;

    let pk_hex = pk_hex.trim().trim_start_matches("0x");
    let bytes = hex::decode(pk_hex)
        .map_err(|_| "KASPA_SIGNER_PRIVATE_KEY must be hex".to_string())?;

    if bytes.len() != 32 {
        return Err(format!("private key must be 32 bytes (got {})", bytes.len()));
    }

    let sk = SecretKey::from_slice(&bytes)
        .map_err(|_| "invalid secp256k1 private key".to_string())?;

    let secp = Secp256k1::new();
    let pk = PublicKey::from_secret_key(&secp, &sk);

    Ok(hex::encode(pk.serialize()))
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
            "note": "Layer 3.1 stabilized. Next: derive real Kaspa address from key + UTXO discovery via kaspad gRPC."
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
