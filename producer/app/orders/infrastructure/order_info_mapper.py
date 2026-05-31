from app.orders.domain.order_info import OrderInfo
from app.orders.infrastructure.order_info_model import OrderInfoModel


class OrderInfoMapper:
    @staticmethod
    def to_model(order: OrderInfo) -> OrderInfoModel:
        return OrderInfoModel(
            client_id=order.client_id,
            card_number=order.card_number,
            total_price=order.total_price,
            restaurant_code=order.restaurant_code,
            transaction_datetime=order.transaction_datetime,
        )

    @staticmethod
    def to_domain(model: OrderInfoModel) -> OrderInfo:
        return OrderInfo(
            client_id=model.client_id,
            card_number=model.card_number,
            total_price=model.total_price,
            restaurant_code=model.restaurant_code,
            transaction_datetime=model.transaction_datetime,
        )
