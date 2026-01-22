use axum::{
    extract::State,
    http::StatusCode,
    response::IntoResponse,
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::net::SocketAddr;

use crate::state::RuntimeState;

pub async fn serve_http(state: RuntimeState) -> Result<(), Box<dyn std::error::Error>> {
    let app = Router::new()
        .route("/healthz", get(healthz))
        .route("/metrics-lite", get(metrics_lite))
        // Task #3: broadcast endpoint (FastAPI -> Axum HTTP)
        .route("/v1/kaspa/broadcast", post(kaspa_broadcast))
        .with_state(state);

    let host = std::env::var("SIDECAR_HTTP_HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let port = std::env::var("SIDECAR_HTTP_PORT").unwrap_or_else(|_| "8080".to_string());
    let addr: SocketAddr = format!("{}:{}", host, port).parse()?;

    println!("[HTTP] listening on http://{}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;
    Ok(())
}

async fn healthz(State(state): State<RuntimeState>) -> impl IntoResponse {
    let connected = state.is_connected();
    let daa = state.daa();
    let daa_ts = state.daa_updated_ts();
    let err_ts = state.last_error_ts();

    let ready = connected && daa_ts > 0;

    let body = json!({
        "status": "ok",
        "ready": ready,
        "connected": connected,
        "virtual_daa_score": daa,
        "last_daa_update_ts": daa_ts,
        "last_error_ts": err_ts,
        "endpoint": std::env::var("KASPAD_GRPC_ENDPOINT").unwrap_or_else(|_| "(env not set)".to_string()),
    });

    if ready {
        (StatusCode::OK, Json(body))
    } else {
        (StatusCode::SERVICE_UNAVAILABLE, Json(body))
    }
}

async fn metrics_lite(State(state): State<RuntimeState>) -> impl IntoResponse {
    let connected = if state.is_connected() { 1 } else { 0 };
    let daa = state.daa();
    let daa_ts = state.daa_updated_ts();
    let err_ts = state.last_error_ts();

    let text = format!(
        "sidecar_connected {}\nsidecar_virtual_daa_score {}\nsidecar_last_daa_update_ts {}\nsidecar_last_error_ts {}\n",
        connected, daa, daa_ts, err_ts
    );

    (StatusCode::OK, text)
}

#[derive(Debug, Deserialize)]
struct KaspaBroadcastRequest {
    refund_id: String,
    to_address: String,
    amount_sompi: u64,
    network: String, // "testnet" for Task #3
}

#[derive(Debug, Serialize)]
struct KaspaBroadcastResponse {
    txid: String,
}

async fn kaspa_broadcast(State(state): State<RuntimeState>, Json(req): Json<KaspaBroadcastRequest>) -> impl IntoResponse {
    // Guardrail: Task #3 is testnet-only at this stage.
    if req.network.to_lowercase() != "testnet" {
        let body = json!({"error": "network_not_allowed", "note": "Task #3 is testnet-only"});
        return (StatusCode::BAD_REQUEST, Json(body));
    }

    // Delegate to runtime/engine (no business logic here).
    // You must implement this call in RuntimeState (or expose an engine function it can call).
    match broadcast_via_runtime_state(&state, &req.refund_id, &req.to_address, req.amount_sompi).await {
        Ok(txid) => (StatusCode::OK, Json(json!(KaspaBroadcastResponse { txid }))),
        Err(e) => {
            let body = json!({"error": "broadcast_failed", "reason": e});
            (StatusCode::BAD_GATEWAY, Json(body))
        }
    }
}

// NOTE:
// This is intentionally a thin wrapper to avoid guessing your kaspa-grpc-core wiring.
// Implement it by calling your existing engine/grpc client to build+sign+broadcast and return txid.
async fn broadcast_via_runtime_state(
    state: &RuntimeState,
    refund_id: &str,
    to_address: &str,
    amount_sompi: u64,
) -> Result<String, String> {
    // Placeholder: fail clearly until wired.
    let _ = (state, refund_id, to_address, amount_sompi);
    Err("broadcast not wired: implement broadcast_via_runtime_state() to call your kaspad gRPC submit/broadcast flow".to_string())
}
