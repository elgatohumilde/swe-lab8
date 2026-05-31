from typing import Protocol
from uuid import UUID

from app.cashback.domain.cashback_info import CashbackInfo
from app.orders.domain.order_info import OrderInfo


class CashbackRepository(Protocol):
    def list_all(self) -> list[CashbackInfo]: ...
    def get_by_client_id(self, client_id: UUID) -> CashbackInfo | None: ...
    def save_or_update_client_info(self, order: OrderInfo) -> None: ...
