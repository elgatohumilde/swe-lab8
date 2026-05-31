from decimal import Decimal
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class CashbackInfoModel(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    client_id: UUID = Field(unique=True)
    available_cashback: Decimal
