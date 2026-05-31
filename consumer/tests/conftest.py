import os
from unittest.mock import MagicMock, patch

os.environ["CONSUMER_DB_URL"] = "sqlite:///test.db"
os.environ["APACHE_KAFKA_SERVER"] = "localhost"
os.environ["APACHE_KAFKA_PORT"] = "9092"
os.environ["APACHE_KAFKA_TOPIC"] = "test-topic"
os.environ["APACHE_KAFKA_GROUP_ID"] = "test-group"
os.environ["CASHBACK_PERCENTAGE"] = "0.01"

_patcher = patch("confluent_kafka.Consumer", return_value=MagicMock())
_patcher.start()
