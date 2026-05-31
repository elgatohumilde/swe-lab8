import os

os.environ["PRODUCER_DB_URL"] = "sqlite:///test.db"
os.environ["APACHE_KAFKA_SERVER"] = "localhost"
os.environ["APACHE_KAFKA_PORT"] = "9092"
os.environ["APACHE_KAFKA_TOPIC"] = "test-topic"
