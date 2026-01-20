mod kaspa;
mod state;
mod http;

use state::RuntimeState;
use tracing::info;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let state = RuntimeState::new();

    // CHANGE THIS TO YOUR DIGITALOCEAN IP WHEN READY
    let kaspad_endpoint = "http://127.0.0.1:16110".to_string();

    tokio::spawn(kaspa::grpc_client::connect_with_retry(kaspad_endpoint));
    tokio::spawn(kaspa::settlement_clock::run(state));
    tokio::spawn(http::serve());

    info!("sidecar started");

    loop {
        tokio::time::sleep(std::time::Duration::from_secs(3600)).await;
    }
}
