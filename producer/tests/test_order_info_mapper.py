from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.orders.domain.order_info import OrderInfo
from app.orders.infrastructure.order_info_mapper import OrderInfoMapper
from app.orders.infrastructure.order_info_model import OrderInfoModel


class TestOrderInfoMapper:
    def test_to_model(self):
        order = OrderInfo(
            client_id=UUID("12345678-1234-5678-1234-567812345678"),
            card_number="1234567890123456",
            total_price=Decimal("100.50"),
            restaurant_code="REST01",
            transaction_datetime=datetime(2024, 1, 1, 12, 0, 0),
        )
        model = OrderInfoMapper.to_model(order)
        assert model.client_id == order.client_id
        assert model.card_number == order.card_number
        assert model.total_price == order.total_price
        assert model.restaurant_code == order.restaurant_code
        assert model.transaction_datetime == order.transaction_datetime

    def test_to_domain(self):
        model = OrderInfoModel(
            client_id=UUID("12345678-1234-5678-1234-567812345678"),
            card_number="1234567890123456",
            total_price=Decimal("100.50"),
            restaurant_code="REST01",
            transaction_datetime=datetime(2024, 1, 1, 12, 0, 0),
        )
        order = OrderInfoMapper.to_domain(model)
        assert order.client_id == model.client_id
        assert order.card_number == model.card_number
        assert order.total_price == model.total_price
        assert order.restaurant_code == model.restaurant_code
        assert order.transaction_datetime == model.transaction_datetime
