use axum::{
    routing::get,
    Router,
    response::IntoResponse,
    Json,
};
use serde_json::json;
use tokio::net::TcpListener;

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
