from decimal import Decimal
from typing import final, override
from uuid import UUID

from sqlmodel import Session, select

from app.cashback.domain.cashback_info import CashbackInfo
from app.cashback.domain.cashback_repository import CashbackRepository
from app.cashback.infrastructure.cashback_info_mapper import CashbackInfoMapper
from app.cashback.infrastructure.cashback_info_model import CashbackInfoModel
from app.common.funcs import load_env
from app.orders.domain.order_info import OrderInfo


@final
class SqlCashbackRepository(CashbackRepository):
    CASHBACK_PERCENTAGE = Decimal(load_env("CASHBACK_PERCENTAGE"))

    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    @override
    def list_all(self) -> list[CashbackInfo]:
        info_models = self.db_session.exec(select(CashbackInfoModel)).all()
        all_info = [CashbackInfoMapper.to_domain(model) for model in info_models]

        return all_info

    @override
    def get_by_client_id(self, client_id: UUID) -> CashbackInfo | None:
        model = self.db_session.exec(
            select(CashbackInfoModel).where(CashbackInfoModel.client_id == client_id)
        ).one_or_none()

        if not model:
            return None

        cashback_info = CashbackInfoMapper.to_domain(model)
        return cashback_info

    @override
    def save_or_update_client_info(self, order: OrderInfo) -> None:
        NEW_CASHBACK = order.total_price * self.CASHBACK_PERCENTAGE

        existing = self.db_session.exec(
            select(CashbackInfoModel).where(
                CashbackInfoModel.client_id == order.client_id
            )
        ).one_or_none()

        if not existing:
            self.db_session.add(
                CashbackInfoModel(
                    client_id=order.client_id,
                    available_cashback=NEW_CASHBACK,
                )
            )
        else:
            existing.available_cashback += NEW_CASHBACK
            self.db_session.add(existing)

        self.db_session.commit()
