from typing import final, override

from app.config.kafka import KAFKA_PRODUCER, KAFKA_TOPIC, kafka_callback
from app.orders.domain.order_info import OrderInfo
from app.orders.domain.order_repository import OrderRepository
from app.orders.domain.order_service import OrderService


@final
class KafkaOrderService(OrderService):
    def __init__(self, order_repository: OrderRepository) -> None:
        self.order_repository = order_repository

    @override
    def receive_order(self, order: OrderInfo) -> None:
        KAFKA_PRODUCER.produce(
            KAFKA_TOPIC,
            value=order.model_dump_json().encode("utf-8"),
            callback=kafka_callback,
        )
        _ = KAFKA_PRODUCER.flush()

        self.order_repository.save(order)

    @override
    def list_orders(self) -> list[OrderInfo]:
        return self.order_repository.list_all()
