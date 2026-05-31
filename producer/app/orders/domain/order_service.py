from typing import Protocol

from app.orders.domain.order_info import OrderInfo


class OrderService(Protocol):
    def receive_order(self, order: OrderInfo) -> None: ...
    def list_orders(self) -> list[OrderInfo]: ...
