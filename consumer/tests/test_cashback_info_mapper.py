from decimal import Decimal
from uuid import UUID

from app.cashback.domain.cashback_info import CashbackInfo
from app.cashback.infrastructure.cashback_info_mapper import CashbackInfoMapper
from app.cashback.infrastructure.cashback_info_model import CashbackInfoModel


class TestCashbackInfoMapper:
    def test_to_domain(self):
        model = CashbackInfoModel(
            client_id=UUID("12345678-1234-5678-1234-567812345678"),
            available_cashback=Decimal("10.50"),
        )
        info = CashbackInfoMapper.to_domain(model)
        assert info.client_id == model.client_id
        assert info.available_cashback == model.available_cashback
