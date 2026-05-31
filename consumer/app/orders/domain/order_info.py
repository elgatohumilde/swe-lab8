from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class OrderInfo(BaseModel):
    client_id: UUID
    card_number: str
    total_price: Decimal
    restaurant_code: str
    transaction_datetime: datetime
