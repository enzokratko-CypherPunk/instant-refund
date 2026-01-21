use axum::{routing::get, Json, Router};
use serde_json::json;
use tokio::net::TcpListener;

fn env_default(key: &str, default: &str) -> String {
    std::env::var(key).unwrap_or_else(|_| default.to_string())
}

async fn healthz() -> Json<serde_json::Value> {
    Json(json!({ "status": "ok" }))
}

async fn debug_wallet() -> Json<serde_json::Value> {
    let network = env_default("KASPA_NETWORK", "mainnet");

    let has_key = std::env::var("KASPA_SIGNER_PRIVATE_KEY").is_ok();

    Json(json!({
        "network": network,
        "wallet_bound": has_key,
        "balance": 0,
        "utxos": [],
        "note": "Layer 3.1 stable. Cryptography + address derivation comes in Layer 3.2."
    }))
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
