from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path

from app.cashback.domain.cashback_service import CashbackService
from app.cashback.infrastructure.impl_config import get_cashback_service

cashback_router = APIRouter(prefix="/cashback", tags=["cashback"])


@cashback_router.get("/")
def list_cashback_per_client(
    cashback_service: Annotated[CashbackService, Depends(get_cashback_service)],
):
    clients_cashback_info = cashback_service.list_clients_cashback_info()
    return {"data": clients_cashback_info}


@cashback_router.get("/{client_id}", responses={404: {"description": "user not found"}})
def get_available_cashback(
    client_id: Annotated[UUID, Path],
    cashback_service: Annotated[CashbackService, Depends(get_cashback_service)],
):
    cashback_info = cashback_service.get_client_cashback_info(client_id)
    if not cashback_info:
        raise HTTPException(
            status_code=404, detail="cashback info not found for given client id"
        )

    return {"data": cashback_info}
