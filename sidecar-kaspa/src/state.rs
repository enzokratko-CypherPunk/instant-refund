#[derive(Clone, Debug)]
pub struct RuntimeState {
    pub started_at: std::time::Instant,
}

impl RuntimeState {
    pub fn new() -> Self {
        Self {
            started_at: std::time::Instant::now(),
        }
    }
}
