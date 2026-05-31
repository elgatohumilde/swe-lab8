from typing import Protocol
from uuid import UUID

from app.cashback.domain.cashback_info import CashbackInfo
from app.orders.domain.order_info import OrderInfo


class CashbackService(Protocol):
    def list_clients_cashback_info(self) -> list[CashbackInfo]: ...
    def get_client_cashback_info(self, client_id: UUID) -> CashbackInfo | None: ...
    def process_order(self, order: OrderInfo) -> None: ...
