from sqlmodel import Session

from app.cashback.domain.cashback_repository import CashbackRepository
from app.cashback.domain.cashback_service import CashbackService
from app.cashback.domain.domain_cashback_service import DomainCashbackService
from app.cashback.infrastructure.sql_cashback_repository import SqlCashbackRepository
from app.config.db_engine import ENGINE


def get_cashback_service() -> CashbackService:
    return DomainCashbackService(cashback_repository=get_cashback_repository())


def get_cashback_repository() -> CashbackRepository:
    return SqlCashbackRepository(get_session())


def get_session() -> Session:
    with Session(ENGINE) as session:
        return session
