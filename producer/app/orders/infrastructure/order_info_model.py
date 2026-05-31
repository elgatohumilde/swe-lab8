from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class OrderInfoModel(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    client_id: UUID
    card_number: str
    total_price: Decimal
    restaurant_code: str
    transaction_datetime: datetime
