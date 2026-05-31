from decimal import Decimal
from unittest.mock import MagicMock
from uuid import UUID

from app.cashback.domain.cashback_info import CashbackInfo
from app.cashback.domain.cashback_repository import CashbackRepository
from app.cashback.domain.domain_cashback_service import DomainCashbackService


class TestDomainCashbackService:
    def test_list_clients_cashback_info(self):
        mock_repo = MagicMock(spec=CashbackRepository)
        mock_repo.list_all.return_value = [
            CashbackInfo(
                client_id=UUID("12345678-1234-5678-1234-567812345678"),
                available_cashback=Decimal("10.00"),
            )
        ]
        service = DomainCashbackService(cashback_repository=mock_repo)
        result = service.list_clients_cashback_info()
        assert len(result) == 1
        assert result[0].available_cashback == Decimal("10.00")

    def test_get_client_cashback_info_found(self):
        mock_repo = MagicMock(spec=CashbackRepository)
        client_id = UUID("12345678-1234-5678-1234-567812345678")
        mock_repo.get_by_client_id.return_value = CashbackInfo(
            client_id=client_id, available_cashback=Decimal("10.00")
        )
        service = DomainCashbackService(cashback_repository=mock_repo)
        result = service.get_client_cashback_info(client_id)
        assert result is not None
        assert result.client_id == client_id

    def test_get_client_cashback_info_not_found(self):
        mock_repo = MagicMock(spec=CashbackRepository)
        mock_repo.get_by_client_id.return_value = None
        service = DomainCashbackService(cashback_repository=mock_repo)
        result = service.get_client_cashback_info(
            UUID("00000000-0000-0000-0000-000000000000")
        )
        assert result is None

    def test_process_order(self):
        mock_repo = MagicMock(spec=CashbackRepository)
        service = DomainCashbackService(cashback_repository=mock_repo)
        order = MagicMock()
        service.process_order(order)
        mock_repo.save_or_update_client_info.assert_called_once_with(order)
