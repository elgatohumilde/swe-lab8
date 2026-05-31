from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch
from uuid import UUID

from app.orders.application.kafka_service import KafkaOrderService
from app.orders.domain.order_info import OrderInfo
from app.orders.domain.order_repository import OrderRepository


class TestKafkaOrderService:
    def test_list_orders_delegates_to_repository(self):
        mock_repo = MagicMock(spec=OrderRepository)
        mock_repo.list_all.return_value = []
        service = KafkaOrderService(order_repository=mock_repo)
        assert service.list_orders() == []
        mock_repo.list_all.assert_called_once()

    @patch("app.orders.application.kafka_service.KAFKA_PRODUCER")
    def test_receive_order_produces_and_saves(self, mock_producer):
        mock_repo = MagicMock(spec=OrderRepository)
        service = KafkaOrderService(order_repository=mock_repo)

        order = OrderInfo(
            client_id=UUID("12345678-1234-5678-1234-567812345678"),
            card_number="1234567890123456",
            total_price=Decimal("100.50"),
            restaurant_code="REST01",
            transaction_datetime=datetime(2024, 1, 1, 12, 0, 0),
        )

        service.receive_order(order)

        mock_producer.produce.assert_called_once()
        call_args = mock_producer.produce.call_args
        assert call_args[0][0] == "test-topic"
        assert call_args[1]["value"] == order.model_dump_json().encode("utf-8")

        mock_producer.flush.assert_called_once()
        mock_repo.save.assert_called_once_with(order)
