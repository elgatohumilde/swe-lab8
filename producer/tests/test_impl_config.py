from unittest.mock import MagicMock, patch

from sqlmodel import Session

from app.orders.application.kafka_service import KafkaOrderService
from app.orders.infrastructure.impl_config import (
    get_order_repository,
    get_order_service,
    get_session,
)
from app.orders.infrastructure.sql_order_repository import SqlOrderRepository


class TestImplConfig:
    @patch("app.orders.infrastructure.impl_config.get_order_repository")
    def test_get_order_service(self, mock_get_repo):
        mock_get_repo.return_value = MagicMock()
        service = get_order_service()
        assert isinstance(service, KafkaOrderService)

    @patch("app.orders.infrastructure.impl_config.get_session")
    def test_get_order_repository(self, mock_get_session):
        mock_session = MagicMock(spec=Session)
        mock_get_session.return_value = mock_session
        repo = get_order_repository()
        assert isinstance(repo, SqlOrderRepository)

    def test_get_session(self):
        session = get_session()
        assert isinstance(session, Session)
