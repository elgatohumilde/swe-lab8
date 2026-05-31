from app.config.kafka import (
    KAFKA_CONSUMER,
    KAFKA_TOPIC,
    load_kafka_consumer_config,
    load_kafka_order_topic,
)


class TestLoadKafkaConsumerConfig:
    def test_load_kafka_consumer_config(self):
        config = load_kafka_consumer_config()
        assert config["bootstrap.servers"] == "localhost:9092"
        assert config["group.id"] == "test-group"
        assert config["auto.offset.reset"] == "earliest"

    def test_load_kafka_order_topic(self):
        assert load_kafka_order_topic() == "test-topic"

    def test_module_level_constants(self):
        assert KAFKA_TOPIC == "test-topic"
        assert KAFKA_CONSUMER is not None
        KAFKA_CONSUMER.subscribe.assert_called_once()
