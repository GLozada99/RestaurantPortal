from django.db.transaction import atomic

from portal.authentication.models import User
from portal.order.models import Order, OrderDish, OrderPromotion, OrderStatus
from portal.order.services.subtract_inventory import (
    SubtractInventoryAPIService
)
from portal.order.services.validate_order import ValidateOrderAPIService


class OrderAPIService:

    @classmethod
    @atomic
    def create(
        cls, data: dict, restaurant_id: int, branch_id: int, user: User
    ):
        ValidateOrderAPIService.validate_data(
            data, branch_id, restaurant_id, user,
        )
        dishes = data.pop('dishes', [])
        promotions = data.pop('promotions', [])
        order = cls.get_instance(data, branch_id, user, dishes, promotions)
        cls.add_dishes_to_order(dishes, order)
        cls.add_promotions_to_order(promotions, order)
        SubtractInventoryAPIService.subtract(order)
        return order

    @classmethod
    def get_instance(
        cls, data: dict, branch_id: int, client: User, dishes, promotions
    ):
        order = Order(
            address=data.get('address'),
            total_cost=cls.calculate_total_price(dishes, promotions),
            client=client,
            status=OrderStatus.objects.get(previous_status=None),
            delivery_type=data.get('delivery_type'),
            branch_id=branch_id,
        )
        order.save()
        return order

    @classmethod
    def calculate_total_price(cls, dishes_data: list, promotions_data: list):
        return (cls.calculate_dishes_price(dishes_data) +
                cls.calculate_promotions_price(promotions_data))

    @classmethod
    def calculate_dishes_price(cls, dishes_data: list):
        dishes_prices = [dish_data['dish'].price for dish_data in dishes_data]
        return cls.calculate_price(dishes_data, dishes_prices)

    @classmethod
    def calculate_promotions_price(cls, promotions_data: list):
        promotions_prices = [
            promotion_data['promotion'].price
            for promotion_data in promotions_data
        ]
        return cls.calculate_price(promotions_data, promotions_prices)

    @staticmethod
    def calculate_price(data: dict, prices):
        return sum((
            price * instance['quantity']
            for instance, price in zip(data, prices)
        ))

    @staticmethod
    def add_dishes_to_order(dishes_data: dict, order: Order):
        for dish_data in dishes_data:
            OrderDish.objects.create(
                order_id=order.id,
                dish_id=dish_data['dish'].id,
                quantity=dish_data['quantity'],
            )

    @staticmethod
    def add_promotions_to_order(promotions_data: dict, order: Order):
        for promotion_data in promotions_data:
            OrderPromotion.objects.create(
                order_id=order.id,
                promotion_id=promotion_data['promotion'].id,
                quantity=promotion_data['quantity'],
            )
