import asyncio
from unittest.mock import MagicMock

import pytest

from app.cashback.application.kafka_listener import consume_kafka


class TestConsumeKafka:
    def test_skip_when_no_message(self):
        consumer = MagicMock()
        service = MagicMock()
        calls = 0

        def poll_side_effect(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls >= 3:
                raise RuntimeError("stop")
            return None

        consumer.poll.side_effect = poll_side_effect

        with pytest.raises(RuntimeError):
            asyncio.run(consume_kafka(consumer, service))

        assert calls == 3
        service.process_order.assert_not_called()

    def test_skip_on_error(self):
        consumer = MagicMock()
        service = MagicMock()
        calls = 0

        def poll_side_effect(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls >= 3:
                raise RuntimeError("stop")
            msg = MagicMock()
            msg.error.return_value = "some error"
            return msg

        consumer.poll.side_effect = poll_side_effect

        with pytest.raises(RuntimeError):
            asyncio.run(consume_kafka(consumer, service))

        service.process_order.assert_not_called()

    def test_skip_when_no_value(self):
        consumer = MagicMock()
        service = MagicMock()
        calls = 0

        def poll_side_effect(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls >= 3:
                raise RuntimeError("stop")
            msg = MagicMock()
            msg.error.return_value = None
            msg.value.return_value = None
            return msg

        consumer.poll.side_effect = poll_side_effect

        with pytest.raises(RuntimeError):
            asyncio.run(consume_kafka(consumer, service))

        service.process_order.assert_not_called()

    def test_processes_valid_order(self):
        consumer = MagicMock()
        service = MagicMock()
        calls = 0

        def poll_side_effect(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls >= 2:
                raise RuntimeError("stop")
            msg = MagicMock()
            msg.error.return_value = None
            msg.value.return_value = (
                b'{"client_id": "12345678-1234-5678-1234-567812345678", '
                b'"card_number": "1234", "total_price": 100.0, '
                b'"restaurant_code": "R01", '
                b'"transaction_datetime": "2024-01-01T00:00:00"}'
            )
            return msg

        consumer.poll.side_effect = poll_side_effect

        with pytest.raises(RuntimeError):
            asyncio.run(consume_kafka(consumer, service))

        service.process_order.assert_called_once()
