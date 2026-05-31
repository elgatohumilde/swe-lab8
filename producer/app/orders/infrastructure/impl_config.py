from sqlmodel import Session

from app.config.db_engine import ENGINE
from app.orders.application.kafka_service import KafkaOrderService
from app.orders.domain.order_repository import OrderRepository
from app.orders.domain.order_service import OrderService
from app.orders.infrastructure.sql_order_repository import SqlOrderRepository


def get_order_service() -> OrderService:
    return KafkaOrderService(order_repository=get_order_repository())


def get_order_repository() -> OrderRepository:
    return SqlOrderRepository(db_session=get_session())


def get_session() -> Session:
    with Session(ENGINE) as session:
        return session
