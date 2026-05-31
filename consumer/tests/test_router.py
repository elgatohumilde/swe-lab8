from decimal import Decimal
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.cashback.application.router import cashback_router
from app.cashback.domain.cashback_service import CashbackService
from app.cashback.infrastructure.impl_config import get_cashback_service


@pytest.fixture
def mock_cashback_service():
    return MagicMock(spec=CashbackService)


@pytest.fixture
def client(mock_cashback_service):
    test_app = FastAPI()
    test_app.include_router(cashback_router)
    test_app.dependency_overrides[get_cashback_service] = lambda: mock_cashback_service
    with TestClient(test_app) as c:
        yield c


class TestRouter:
    def test_list_cashback_empty(self, client, mock_cashback_service):
        mock_cashback_service.list_clients_cashback_info.return_value = []
        response = client.get("/cashback/")
        assert response.status_code == 200
        assert response.json() == {"data": []}

    def test_list_cashback_with_data(self, client, mock_cashback_service):
        mock_cashback_service.list_clients_cashback_info.return_value = [
            {
                "client_id": "12345678-1234-5678-1234-567812345678",
                "available_cashback": Decimal("10.00"),
            }
        ]
        response = client.get("/cashback/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 1

    def test_get_cashback_found(self, client, mock_cashback_service):
        client_id = UUID("12345678-1234-5678-1234-567812345678")
        mock_cashback_service.get_client_cashback_info.return_value = {
            "client_id": str(client_id),
            "available_cashback": Decimal("10.00"),
        }
        response = client.get(f"/cashback/{client_id}")
        assert response.status_code == 200

    def test_get_cashback_not_found(self, client, mock_cashback_service):
        mock_cashback_service.get_client_cashback_info.return_value = None
        response = client.get("/cashback/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
        assert response.json()["detail"] == "cashback info not found for given client id"
