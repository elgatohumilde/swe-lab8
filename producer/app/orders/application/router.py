from typing import Annotated

from fastapi import APIRouter, Depends

from app.orders.domain.order_info import OrderInfo
from app.orders.domain.order_service import OrderService
from app.orders.infrastructure.impl_config import get_order_service

orders_router = APIRouter(prefix="/orders", tags=["orders"])


@orders_router.post("/", status_code=202)
def receive_order(
    order: OrderInfo, order_service: Annotated[OrderService, Depends(get_order_service)]
):
    order_service.receive_order(order)
    return {"message": "order received"}


@orders_router.get("/")
def list_orders(order_service: Annotated[OrderService, Depends(get_order_service)]):
    orders = order_service.list_orders()
    return {"data": orders}
