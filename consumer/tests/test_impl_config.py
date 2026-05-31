from unittest.mock import MagicMock, patch

from sqlmodel import Session

from app.cashback.domain.domain_cashback_service import DomainCashbackService
from app.cashback.infrastructure.impl_config import (
    get_cashback_repository,
    get_cashback_service,
    get_session,
)
from app.cashback.infrastructure.sql_cashback_repository import (
    SqlCashbackRepository,
)


class TestImplConfig:
    @patch("app.cashback.infrastructure.impl_config.get_cashback_repository")
    def test_get_cashback_service(self, mock_get_repo):
        mock_get_repo.return_value = MagicMock()
        service = get_cashback_service()
        assert isinstance(service, DomainCashbackService)

    @patch("app.cashback.infrastructure.impl_config.get_session")
    def test_get_cashback_repository(self, mock_get_session):
        mock_get_session.return_value = MagicMock(spec=Session)
        repo = get_cashback_repository()
        assert isinstance(repo, SqlCashbackRepository)

    def test_get_session(self):
        session = get_session()
        assert isinstance(session, Session)
