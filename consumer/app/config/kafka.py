from typing import Final

from confluent_kafka import Consumer

from app.common.funcs import load_env


def load_kafka_consumer_config() -> dict[str, str]:
    kafka_server = load_env("APACHE_KAFKA_SERVER")
    kafka_port = load_env("APACHE_KAFKA_PORT")
    kafka_group_id = load_env("APACHE_KAFKA_GROUP_ID")

    return {
        "bootstrap.servers": f"{kafka_server}:{kafka_port}",
        "group.id": kafka_group_id,
        "auto.offset.reset": "earliest",
    }


def load_kafka_order_topic() -> str:
    kafka_topic = load_env("APACHE_KAFKA_TOPIC")

    return kafka_topic


KAFKA_CONSUMER: Final[Consumer] = Consumer(load_kafka_consumer_config())
KAFKA_TOPIC: Final[str] = load_kafka_order_topic()

KAFKA_CONSUMER.subscribe([KAFKA_TOPIC])
