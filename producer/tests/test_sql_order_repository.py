from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytest
from sqlmodel import SQLModel, Session, create_engine

from app.orders.domain.order_info import OrderInfo
from app.orders.infrastructure.order_info_model import OrderInfoModel
from app.orders.infrastructure.sql_order_repository import SqlOrderRepository


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


class TestSqlOrderRepository:
    def test_save_and_list_all(self, session):
        repo = SqlOrderRepository(session)
        order = OrderInfo(
            client_id=UUID("12345678-1234-5678-1234-567812345678"),
            card_number="1234567890123456",
            total_price=Decimal("100.50"),
            restaurant_code="REST01",
            transaction_datetime=datetime(2024, 1, 1, 12, 0, 0),
        )
        repo.save(order)
        orders = repo.list_all()
        assert len(orders) == 1
        assert orders[0].client_id == order.client_id
        assert orders[0].total_price == order.total_price
        assert orders[0].restaurant_code == order.restaurant_code

    def test_list_all_empty(self, session):
        repo = SqlOrderRepository(session)
        assert repo.list_all() == []

    def test_save_multiple_orders(self, session):
        repo = SqlOrderRepository(session)
        order1 = OrderInfo(
            client_id=UUID("11111111-1111-1111-1111-111111111111"),
            card_number="1111111111111111",
            total_price=Decimal("50.00"),
            restaurant_code="REST01",
            transaction_datetime=datetime(2024, 1, 1, 12, 0, 0),
        )
        order2 = OrderInfo(
            client_id=UUID("22222222-2222-2222-2222-222222222222"),
            card_number="2222222222222222",
            total_price=Decimal("75.00"),
            restaurant_code="REST02",
            transaction_datetime=datetime(2024, 1, 1, 13, 0, 0),
        )
        repo.save(order1)
        repo.save(order2)
        orders = repo.list_all()
        assert len(orders) == 2
