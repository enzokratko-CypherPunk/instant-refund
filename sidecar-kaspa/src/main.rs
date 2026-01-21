use axum::{routing::get, Json, Router};
use serde::Serialize;
use std::{env, net::SocketAddr};

use tokio_stream::StreamExt as _;

use kaspa_grpc_core::protowire::{
    GetUtxosByAddressesRequestMessage,
    GetUtxosByAddressesResponseMessage,
    KaspadRequest,
};
use kaspa_grpc_core::protowire::kaspad_response::Payload as KaspadResponsePayload;
use kaspa_grpc_core::protowire::rpc_client::RpcClient;

#[derive(Serialize)]
struct HealthResponse {
    status: &'static str,
}

#[derive(Serialize)]
struct WalletResponse {
    network: String,
    address: String,
    balance: u64,
    utxo_count: usize,
    utxos: Vec<WalletUtxo>,
    error: Option<String>,
}

#[derive(Serialize)]
struct WalletUtxo {
    outpoint_txid: String,
    outpoint_index: u32,
    amount: u64,
}

fn env_required(key: &str) -> Result<String, String> {
    env::var(key).map_err(|_| format!("Missing required env var: {}", key))
}

fn env_default(key: &str, default: &str) -> String {
    env::var(key).unwrap_or_else(|_| default.to_string())
}

async fn healthz() -> Json<HealthResponse> {
    Json(HealthResponse { status: "ok" })
}

async fn debug_wallet() -> Json<WalletResponse> {
    let network = env_default("KASPA_NETWORK", "mainnet");
    if network.to_lowercase() != "mainnet" {
        return Json(WalletResponse {
            network,
            address: "UNCONFIGURED".to_string(),
            balance: 0,
            utxo_count: 0,
            utxos: vec![],
            error: Some("KASPA_NETWORK must be 'mainnet'".to_string()),
        });
    }

    let address = match env_required("KASPA_WALLET_ADDRESS") {
        Ok(v) => v,
        Err(e) => {
            return Json(WalletResponse {
                network,
                address: "UNCONFIGURED".to_string(),
                balance: 0,
                utxo_count: 0,
                utxos: vec![],
                error: Some(e),
            })
        }
    };

    let endpoint = match env_required("KASPAD_GRPC_ENDPOINT") {
        Ok(v) => v,
        Err(e) => {
            return Json(WalletResponse {
                network,
                address,
                balance: 0,
                utxo_count: 0,
                utxos: vec![],
                error: Some(e),
            })
        }
    };

    let req_msg = GetUtxosByAddressesRequestMessage {
        addresses: vec![address.clone()],
    };

    let kaspad_req: KaspadRequest = req_msg.into();

    let mut client = match RpcClient::connect(endpoint.clone()).await {
        Ok(c) => c,
        Err(e) => {
            return Json(WalletResponse {
                network,
                address,
                balance: 0,
                utxo_count: 0,
                utxos: vec![],
                error: Some(format!("RpcClient::connect failed: {}", e)),
            })
        }
    };

    let outbound = tokio_stream::iter(vec![kaspad_req]);

    let mut inbound = match client.message_stream(outbound).await {
        Ok(resp) => resp.into_inner(),
        Err(e) => {
            return Json(WalletResponse {
                network,
                address,
                balance: 0,
                utxo_count: 0,
                utxos: vec![],
                error: Some(format!("message_stream failed: {}", e)),
            })
        }
    };

    let msg = match inbound.message().await {
        Ok(Some(m)) => m,
        Ok(None) => {
            return Json(WalletResponse {
                network,
                address,
                balance: 0,
                utxo_count: 0,
                utxos: vec![],
                error: Some("No response from kaspad".to_string()),
            })
        }
        Err(e) => {
            return Json(WalletResponse {
                network,
                address,
                balance: 0,
                utxo_count: 0,
                utxos: vec![],
                error: Some(format!("Read error: {}", e)),
            })
        }
    };

    let Some(KaspadResponsePayload::GetUtxosByAddressesResponse(resp)) = msg.payload else {
        return Json(WalletResponse {
            network,
            address,
            balance: 0,
            utxo_count: 0,
            utxos: vec![],
            error: Some("Unexpected response payload".to_string()),
        });
    };

    // ✅ FIX IS HERE — ignore extra fields safely
    let GetUtxosByAddressesResponseMessage { entries, .. } = resp;

    let mut balance: u64 = 0;
    let mut utxos = Vec::new();

    for e in entries.iter() {
        if let Some(utxo_entry) = &e.utxo_entry {
            balance = balance.saturating_add(utxo_entry.amount);
            if utxos.len() < 50 {
                let (txid, index) = if let Some(op) = &e.outpoint {
                    (op.transaction_id.clone(), op.index)
                } else {
                    ("".to_string(), 0)
                };
                utxos.push(WalletUtxo {
                    outpoint_txid: txid,
                    outpoint_index: index,
                    amount: utxo_entry.amount,
                });
            }
        }
    }

    Json(WalletResponse {
        network,
        address,
        balance,
        utxo_count: entries.len(),
        utxos,
        error: None,
    })
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let port: u16 = env_default("SIDECAR_HTTP_PORT", "8080").parse().unwrap_or(8080);
    let addr = SocketAddr::from(([0, 0, 0, 0], port));

    let app = Router::new()
        .route("/healthz", get(healthz))
        .route("/debug/wallet", get(debug_wallet));

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;
    Ok(())
}
