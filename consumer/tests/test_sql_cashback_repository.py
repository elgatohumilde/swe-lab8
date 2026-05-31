from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytest
from sqlmodel import SQLModel, Session, create_engine

from app.cashback.infrastructure.cashback_info_model import CashbackInfoModel
from app.cashback.infrastructure.sql_cashback_repository import (
    SqlCashbackRepository,
)
from app.orders.domain.order_info import OrderInfo


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


class TestSqlCashbackRepository:
    def test_list_all_empty(self, session):
        repo = SqlCashbackRepository(session)
        assert repo.list_all() == []

    def test_save_new_client(self, session):
        repo = SqlCashbackRepository(session)
        order = OrderInfo(
            client_id=UUID("12345678-1234-5678-1234-567812345678"),
            card_number="1234567890123456",
            total_price=Decimal("200.00"),
            restaurant_code="REST01",
            transaction_datetime=datetime(2024, 1, 1, 12, 0, 0),
        )
        repo.save_or_update_client_info(order)

        info = repo.get_by_client_id(order.client_id)
        assert info is not None
        assert info.client_id == order.client_id
        assert info.available_cashback == Decimal("2.00")

    def test_update_existing_client(self, session):
        repo = SqlCashbackRepository(session)
        client_id = UUID("12345678-1234-5678-1234-567812345678")

        order1 = OrderInfo(
            client_id=client_id,
            card_number="1234567890123456",
            total_price=Decimal("200.00"),
            restaurant_code="REST01",
            transaction_datetime=datetime(2024, 1, 1, 12, 0, 0),
        )
        repo.save_or_update_client_info(order1)

        order2 = OrderInfo(
            client_id=client_id,
            card_number="1234567890123456",
            total_price=Decimal("100.00"),
            restaurant_code="REST01",
            transaction_datetime=datetime(2024, 1, 1, 12, 0, 0),
        )
        repo.save_or_update_client_info(order2)

        info = repo.get_by_client_id(client_id)
        assert info is not None
        assert info.available_cashback == Decimal("3.00")

    def test_get_by_client_id_not_found(self, session):
        repo = SqlCashbackRepository(session)
        result = repo.get_by_client_id(
            UUID("00000000-0000-0000-0000-000000000000")
        )
        assert result is None
