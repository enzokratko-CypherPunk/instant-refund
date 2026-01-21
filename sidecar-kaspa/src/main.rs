use axum::{
    routing::get,
    Router,
    response::IntoResponse,
    Json,
};
use std::net::SocketAddr;
use serde_json::json;

async fn healthz() -> impl IntoResponse {
    Json(json!({ "status": "ok" }))
}

async fn debug_wallet() -> impl IntoResponse {
    Json(json!({
        "network": "mainnet",
        "address": "UNRESOLVED",
        "utxos": [],
        "balance": 0
    }))
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/healthz", get(healthz))
        .route("/debug/wallet", get(debug_wallet));

    let port = std::env::var("SIDECAR_HTTP_PORT")
        .unwrap_or_else(|_| "8080".to_string())
        .parse::<u16>()
        .expect("invalid port");

    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    println!("Sidecar listening on {}", addr);

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}
