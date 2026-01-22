use axum::{
    routing::get,
    Router,
    Json,
};
use serde::Serialize;
use serde_json::json;
use std::net::SocketAddr;
use tokio::net::{TcpListener, TcpStream};
use tokio::time::{timeout, Duration};

#[derive(Serialize)]
struct HealthResponse {
    status: &'static str,
}

#[derive(Serialize)]
struct WalletDebugResponse {
    network: &'static str,
    address: &'static str,
    wallet_bound: bool,
    balance: u64,
    utxos: Vec<String>,
}

async fn healthz() -> Json<HealthResponse> {
    Json(HealthResponse { status: "ok" })
}

async fn debug_wallet() -> Json<WalletDebugResponse> {
    Json(WalletDebugResponse {
        network: "mainnet",
        address: "UNRESOLVED",
        wallet_bound: false,
        balance: 0,
        utxos: vec![],
    })
}

async fn debug_kaspad_connect() -> Json<serde_json::Value> {
    let host = std::env::var("KASPA_WRPC_HOST").unwrap_or_else(|_| "10.17.0.5".to_string());
    let port: u16 = std::env::var("KASPA_WRPC_PORT")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(16110);

    let addr = format!("{}:{}", host, port);

    match timeout(Duration::from_secs(3), TcpStream::connect(addr.clone())).await {
        Ok(Ok(_)) => Json(json!({
            "status": "ok",
            "message": format!("Connected to kaspad wRPC at {}", addr)
        })),
        Ok(Err(e)) => Json(json!({
            "status": "error",
            "message": format!("Failed to connect to kaspad at {}", addr),
            "error": e.to_string()
        })),
        Err(_) => Json(json!({
            "status": "error",
            "message": format!("Timed out connecting to kaspad at {}", addr)
        })),
    }
}

#[tokio::main]
async fn main() {
    let app = Router::new().nest(
        "/sidecar",
        Router::new()
            .route("/healthz", get(healthz))
            .route("/debug/wallet", get(debug_wallet))
            .route("/debug/kaspad-connect", get(debug_kaspad_connect)),
    );

    let port: u16 = std::env::var("SIDECAR_HTTP_PORT")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(8080);

    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    let listener = TcpListener::bind(addr)
        .await
        .expect("failed to bind TCP listener");

    axum::serve(listener, app)
        .await
        .expect("sidecar server crashed");
}
