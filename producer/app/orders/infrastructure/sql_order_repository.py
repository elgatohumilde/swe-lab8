from typing import final, override

from sqlmodel import Session, select

from app.orders.domain.order_info import OrderInfo
from app.orders.domain.order_repository import OrderRepository
from app.orders.infrastructure.order_info_mapper import OrderInfoMapper
from app.orders.infrastructure.order_info_model import OrderInfoModel


@final
class SqlOrderRepository(OrderRepository):
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    @override
    def list_all(self) -> list[OrderInfo]:
        order_models = self.db_session.exec(select(OrderInfoModel)).all()
        orders = [OrderInfoMapper.to_domain(model) for model in order_models]

        return orders

    @override
    def save(self, order: OrderInfo) -> None:
        order_model = OrderInfoMapper.to_model(order)

        self.db_session.add(order_model)
        self.db_session.commit()
