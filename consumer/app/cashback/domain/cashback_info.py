from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CashbackInfo(BaseModel):
    client_id: UUID
    available_cashback: Decimal
