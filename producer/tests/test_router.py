from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.orders.domain.order_info import OrderInfo
from app.orders.domain.order_service import OrderService
from app.orders.infrastructure.impl_config import get_order_service


@pytest.fixture
def mock_order_service():
    return MagicMock(spec=OrderService)


@pytest.fixture
def client(mock_order_service):
    app.dependency_overrides[get_order_service] = lambda: mock_order_service
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


class TestRouter:
    def test_health(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_receive_order(self, client, mock_order_service):
        payload = {
            "client_id": "12345678-1234-5678-1234-567812345678",
            "card_number": "1234567890123456",
            "total_price": 100.50,
            "restaurant_code": "REST01",
            "transaction_datetime": "2024-01-01T12:00:00",
        }
        response = client.post("/orders/", json=payload)
        assert response.status_code == 202
        assert response.json() == {"message": "order received"}
        mock_order_service.receive_order.assert_called_once()

    def test_list_orders_empty(self, client, mock_order_service):
        mock_order_service.list_orders.return_value = []
        response = client.get("/orders/")
        assert response.status_code == 200
        assert response.json() == {"data": []}

    def test_list_orders_with_data(self, client, mock_order_service):
        order = OrderInfo(
            client_id=UUID("12345678-1234-5678-1234-567812345678"),
            card_number="1234567890123456",
            total_price=Decimal("100.50"),
            restaurant_code="REST01",
            transaction_datetime=datetime(2024, 1, 1, 12, 0, 0),
        )
        mock_order_service.list_orders.return_value = [order]
        response = client.get("/orders/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 1
        assert data["data"][0]["total_price"] == "100.50"
