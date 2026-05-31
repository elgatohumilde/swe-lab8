from decimal import Decimal
from uuid import UUID

from app.cashback.domain.cashback_info import CashbackInfo


class TestCashbackInfo:
    def test_create_cashback_info(self):
        info = CashbackInfo(
            client_id=UUID("12345678-1234-5678-1234-567812345678"),
            available_cashback=Decimal("10.50"),
        )
        assert info.client_id == UUID("12345678-1234-5678-1234-567812345678")
        assert info.available_cashback == Decimal("10.50")
