from typing import Final

from confluent_kafka import KafkaError, Message, Producer

from app.common.funcs import load_env
from app.common.logger import APP_LOGGER


def load_kafka_producer_config() -> dict[str, str]:
    kafka_server = load_env("APACHE_KAFKA_SERVER")
    kafka_port = load_env("APACHE_KAFKA_PORT")

    return {
        "bootstrap.servers": f"{kafka_server}:{kafka_port}",
    }


def load_kafka_order_topic() -> str:
    kafka_topic = load_env("APACHE_KAFKA_TOPIC")

    return kafka_topic


def kafka_callback(err: KafkaError | None, msg: Message):
    if err is not None:
        APP_LOGGER.warning(f"Kafka delivery failed: {err}")
        return

    APP_LOGGER.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")


KAFKA_PRODUCER: Final[Producer] = Producer(load_kafka_producer_config())
KAFKA_TOPIC: Final[str] = load_kafka_order_topic()
