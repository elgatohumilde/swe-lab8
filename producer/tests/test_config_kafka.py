from unittest.mock import MagicMock

from app.config.kafka import (
    KAFKA_PRODUCER,
    KAFKA_TOPIC,
    kafka_callback,
    load_kafka_order_topic,
    load_kafka_producer_config,
)


class TestLoadKafkaProducerConfig:
    def test_load_kafka_producer_config(self):
        config = load_kafka_producer_config()
        assert config["bootstrap.servers"] == "localhost:9092"

    def test_load_kafka_order_topic(self):
        assert load_kafka_order_topic() == "test-topic"

    def test_kafka_callback_success(self):
        msg = MagicMock()
        msg.topic.return_value = "test-topic"
        msg.partition.return_value = 0
        kafka_callback(None, msg)
        msg.topic.assert_called_once()
        msg.partition.assert_called_once()

    def test_kafka_callback_error(self):
        err = MagicMock()
        msg = MagicMock()
        kafka_callback(err, msg)

    def test_module_level_constants(self):
        assert KAFKA_TOPIC == "test-topic"
        assert KAFKA_PRODUCER is not None
