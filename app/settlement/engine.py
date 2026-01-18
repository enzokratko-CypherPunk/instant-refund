from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.models import Refund, RefundState

# IMPORT your existing Kaspa RPC client
from app.kaspa.client.rpc_pb2_grpc import RPCStub
from app.kaspa.client.rpc_pb2 import SubmitTransactionRequest
import grpc
import os


@dataclass
class SettlementResult:
    success: bool
    settlement_tx_id: Optional[str]
    finalized_at: Optional[datetime]
    failure_reason: Optional[str] = None


class SettlementEngine(ABC):
    @abstractmethod
    def settle_refund(self, refund: Refund) -> SettlementResult:
        pass


class KaspaSettlementEngine(SettlementEngine):
    """
    REAL Kaspa on-chain settlement.
    """

    def __init__(self):
        kaspa_rpc_url = os.getenv("KASPA_RPC_URL", "127.0.0.1:16110")
        self.channel = grpc.insecure_channel(kaspa_rpc_url)
        self.stub = RPCStub(self.channel)

    def settle_refund(self, refund: Refund) -> SettlementResult:
        try:
            # NOTE:
            # This assumes you already know how to construct a raw tx
            # from your earlier experiments. We are intentionally
            # keeping this thin and explicit.

            request = SubmitTransactionRequest(
                # placeholder — your existing tx-building logic plugs here
            )

            response = self.stub.SubmitTransaction(request)

            refund.state = RefundState.SETTLED
            refund.updated_at = datetime.utcnow()

            return SettlementResult(
                success=True,
                settlement_tx_id=response.transaction_id,
                finalized_at=None,  # finality comes in Step 2
            )

        except Exception as e:
            refund.state = RefundState.FAILED
            refund.updated_at = datetime.utcnow()

            return SettlementResult(
                success=False,
                settlement_tx_id=None,
                finalized_at=None,
                failure_reason=str(e),
            )
