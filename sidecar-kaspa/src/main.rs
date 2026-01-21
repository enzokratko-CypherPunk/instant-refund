use axum::{routing::get, Router, response::IntoResponse, Json};
use serde_json::json;
use tokio::net::TcpListener;

use secp256k1::{Secp256k1, SecretKey, PublicKey};
use hex;

async fn healthz() -> impl IntoResponse {
    Json(json!({ "status": "ok" }))
}

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

async fn debug_wallet() -> impl IntoResponse {
    let wallet_id = match derive_wallet_id() {
        Ok(w) => w,
        Err(e) => {
            return Json(json!({
                "network": "mainnet",
                "wallet_id": "UNRESOLVED",
                "balance": 0,
                "utxos": [],
                "error": e
            })).into_response();
        }
    };

    Json(json!({
        "network": "mainnet",
        "wallet_id": wallet_id,
        "balance": 0,
        "utxos": [],
        "note": "UTXO discovery will be wired in Layer 3.1b"
    })).into_response()
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/healthz", get(healthz))
        .route("/debug/wallet", get(debug_wallet));

    let port = std::env::var("SIDECAR_HTTP_PORT")
        .unwrap_or_else(|_| "8080".to_string());

    let addr = format!("0.0.0.0:{}", port);
    let listener = TcpListener::bind(&addr)
        .await
        .expect("failed to bind listener");

    println!("Sidecar listening on {}", addr);

    axum::serve(listener, app)
        .await
        .expect("server error");
}
