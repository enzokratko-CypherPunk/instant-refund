use axum::{
    routing::get,
    Router,
    Json,
};
use serde::Serialize;
use std::net::SocketAddr;
use tokio::net::TcpListener;

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

#[tokio::main]
async fn main() {
    let app = Router::new().nest(
        "/sidecar",
        Router::new()
            .route("/healthz", get(healthz))
            .route("/debug/wallet", get(debug_wallet)),
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
