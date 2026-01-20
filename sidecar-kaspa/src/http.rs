use axum::{routing::get, Router};
use tokio::net::TcpListener;
use tracing::info;

async fn healthz() -> &'static str {
    "ok"
}

pub async fn serve() {
    let app = Router::new().route("/healthz", get(healthz));

    let addr = "0.0.0.0:8080";
    let listener = TcpListener::bind(addr).await.unwrap();

    info!("healthz listening on {}", addr);

    axum::serve(listener, app).await.unwrap();
}
