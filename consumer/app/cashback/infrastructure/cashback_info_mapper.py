from app.cashback.domain.cashback_info import CashbackInfo
from app.cashback.infrastructure.cashback_info_model import CashbackInfoModel


class CashbackInfoMapper:
    @staticmethod
    def to_domain(model: CashbackInfoModel) -> CashbackInfo:
        return CashbackInfo(
            client_id=model.client_id,
            available_cashback=model.available_cashback,
        )
