from typing import Protocol

from app.orders.domain.order_info import OrderInfo


class OrderRepository(Protocol):
    def list_all(self) -> list[OrderInfo]: ...
    def save(self, order: OrderInfo) -> None: ...
