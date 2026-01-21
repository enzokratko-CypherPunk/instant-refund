use axum::{routing::get, Json, Router, response::IntoResponse};
use serde_json::json;
use tokio::net::TcpListener;

use secp256k1::{Secp256k1, SecretKey, PublicKey};

use kaspa_addresses::{Address, Prefix, Version};
use kaspa_consensus_core::network::NetworkType;

use blake2::{Blake2b512, Digest};
use ripemd::{Ripemd160};

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

fn derive_kaspa_address_from_privkey() -> Result<String, String> {
    let pk_hex = std::env::var("KASPA_SIGNER_PRIVATE_KEY")
        .map_err(|_| "missing env var KASPA_SIGNER_PRIVATE_KEY".to_string())?;

    let pk_hex = pk_hex.trim().trim_start_matches("0x");
    let priv_bytes = hex::decode(pk_hex)
        .map_err(|_| "KASPA_SIGNER_PRIVATE_KEY must be hex".to_string())?;

    if priv_bytes.len() != 32 {
        return Err(format!("private key must be 32 bytes (got {})", priv_bytes.len()));
    }

    let sk = SecretKey::from_slice(&priv_bytes)
        .map_err(|_| "invalid secp256k1 private key".to_string())?;

    let secp = Secp256k1::new();
    let pk = PublicKey::from_secret_key(&secp, &sk);
    let pk_bytes = pk.serialize();

    // Kaspa address payload = RIPEMD160(BLAKE2b256(pubkey))
    let blake_hash = Blake2b512::digest(&pk_bytes);
    let mut ripemd = Ripemd160::new();
    ripemd.update(&blake_hash[..32]);
    let payload = ripemd.finalize();

    let address = Address::new(
        Prefix::Mainnet,
        Version::PubKey,
        &payload,
    );

    Ok(address.to_string())
}

async fn healthz() -> impl IntoResponse {
    Json(json!({ "status": "ok" }))
}

async fn debug_wallet() -> impl IntoResponse {
    let network = env_default("KASPA_NETWORK", "mainnet");

    if let Err(e) = require_mainnet() {
        return Json(json!({
            "network": network,
            "address": "UNRESOLVED",
            "wallet_bound": false,
            "balance": 0,
            "utxos": [],
            "error": e
        }));
    }

    match derive_kaspa_address_from_privkey() {
        Ok(address) => Json(json!({
            "network": "mainnet",
            "address": address,
            "wallet_bound": true,
            "balance": 0,
            "utxos": [],
            "note": "Layer 3.2A complete: canonical Kaspa address derived."
        })),
        Err(e) => Json(json!({
            "network": "mainnet",
            "address": "UNRESOLVED",
            "wallet_bound": false,
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
        .expect("failed to bind");

    println!("Sidecar listening on {}", addr);

    axum::serve(listener, app)
        .await
        .expect("server failed");
}
