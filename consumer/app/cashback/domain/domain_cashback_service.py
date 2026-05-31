from typing import final, override
from uuid import UUID

from app.cashback.domain.cashback_info import CashbackInfo
from app.cashback.domain.cashback_repository import CashbackRepository
from app.cashback.domain.cashback_service import CashbackService
from app.orders.domain.order_info import OrderInfo


@final
class DomainCashbackService(CashbackService):
    def __init__(self, cashback_repository: CashbackRepository) -> None:
        self.cashback_repository = cashback_repository

    @override
    def list_clients_cashback_info(self) -> list[CashbackInfo]:
        return self.cashback_repository.list_all()

    @override
    def get_client_cashback_info(self, client_id: UUID) -> CashbackInfo | None:
        return self.cashback_repository.get_by_client_id(client_id)

    @override
    def process_order(self, order: OrderInfo) -> None:
        self.cashback_repository.save_or_update_client_info(order)
