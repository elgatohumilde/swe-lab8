from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.orders.domain.order_info import OrderInfo


class TestOrderInfo:
    def test_create_order_info(self):
        order = OrderInfo(
            client_id=UUID("12345678-1234-5678-1234-567812345678"),
            card_number="1234567890123456",
            total_price=Decimal("100.50"),
            restaurant_code="REST01",
            transaction_datetime=datetime(2024, 1, 1, 12, 0, 0),
        )
        assert order.client_id == UUID("12345678-1234-5678-1234-567812345678")
        assert order.card_number == "1234567890123456"
        assert order.total_price == Decimal("100.50")
        assert order.restaurant_code == "REST01"
        assert order.transaction_datetime == datetime(2024, 1, 1, 12, 0, 0)

    def test_model_dump_json(self):
        order = OrderInfo(
            client_id=UUID("12345678-1234-5678-1234-567812345678"),
            card_number="1234567890123456",
            total_price=Decimal("100.50"),
            restaurant_code="REST01",
            transaction_datetime=datetime(2024, 1, 1, 12, 0, 0),
        )
        data = order.model_dump_json()
        assert "12345678-1234-5678-1234-567812345678" in data
        assert "100.50" in data

    def test_model_validate_json(self):
        json_str = (
            '{"client_id": "12345678-1234-5678-1234-567812345678", '
            '"card_number": "1234567890123456", '
            '"total_price": 100.50, '
            '"restaurant_code": "REST01", '
            '"transaction_datetime": "2024-01-01T12:00:00"}'
        )
        order = OrderInfo.model_validate_json(json_str)
        assert order.client_id == UUID("12345678-1234-5678-1234-567812345678")
        assert order.total_price == Decimal("100.50")
