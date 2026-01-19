import os
import time
from datetime import datetime, timezone, timedelta
from app.db import connect, init_schema

POLL_SECONDS = int(os.getenv("WORKER_POLL_SECONDS", "2"))

def claim_next_job():
    """
    Claim one queued job using SKIP LOCKED so multiple workers can run safely.
    """
    sql = """
    WITH next_job AS (
      SELECT job_id
      FROM settlement_jobs
      WHERE state IN ('queued', 'failed_retryable')
        AND next_run_at <= NOW()
      ORDER BY next_run_at ASC, job_id ASC
      FOR UPDATE SKIP LOCKED
      LIMIT 1
    )
    UPDATE settlement_jobs j
    SET state = 'processing',
        locked_at = NOW(),
        updated_at = NOW()
    FROM next_job
    WHERE j.job_id = next_job.job_id
    RETURNING j.*;
    """
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            row = cur.fetchone()
        conn.commit()
        return row

def mark_retryable(job_id: int, error: str, backoff_seconds: int = 10):
    sql = """
    UPDATE settlement_jobs
    SET state = 'failed_retryable',
        attempts = attempts + 1,
        next_run_at = NOW() + (%s || ' seconds')::interval,
        last_error = %s,
        updated_at = NOW()
    WHERE job_id = %s;
    """
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (backoff_seconds, error[:2000], job_id))
        conn.commit()

def mark_broadcast(job_id: int, refund_id: str, txid: str):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE settlement_jobs
                SET state = 'broadcast',
                    last_error = NULL,
                    updated_at = NOW()
                WHERE job_id = %s;
                """,
                (job_id,)
            )
            cur.execute(
                """
                UPDATE refunds
                SET settlement_state = 'broadcast',
                    txid = %s,
                    last_error = NULL
                WHERE refund_id = %s;
                """,
                (txid, refund_id)
            )
        conn.commit()

def main():
    # Ensure tables exist (safe to call repeatedly)
    init_schema()

    print("instant-refund-worker: started")
    while True:
        job = None
        try:
            job = claim_next_job()
            if not job:
                time.sleep(POLL_SECONDS)
                continue

            # Placeholder: real kaspad RPC signing+broadcast is the next implementation step.
            # For now, simulate "broadcast" with a deterministic placeholder txid.
            refund_id = job["refund_id"]
            fake_txid = "txid_stub_" + str(job["job_id"])

            mark_broadcast(job["job_id"], refund_id, fake_txid)
            print(f"broadcasted (stub): job_id={job['job_id']} refund_id={refund_id} txid={fake_txid}")

        except Exception as e:
            if job and "job_id" in job:
                mark_retryable(job["job_id"], str(e), backoff_seconds=10)
            else:
                print(f"worker error (no job claimed): {e}")
                time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()
