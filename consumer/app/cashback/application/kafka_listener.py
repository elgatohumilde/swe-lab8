import asyncio

from confluent_kafka import Consumer

from app.cashback.domain.cashback_service import CashbackService
from app.common.logger import APP_LOGGER
from app.orders.domain.order_info import OrderInfo


async def consume_kafka(consumer: Consumer, cashback_service: CashbackService) -> None:
    while True:
        message = await asyncio.to_thread(consumer.poll, 1.0)
        if not message:
            continue

        if message.error():
            APP_LOGGER.warning(f"Kafka error: {message.error()}")
            continue

        msg_value = message.value()
        if not msg_value:
            continue

        order = OrderInfo.model_validate_json(msg_value)
        APP_LOGGER.info("received order")

        cashback_service.process_order(order)
