from django.contrib.auth.models import AnonymousUser
from rest_framework.serializers import ValidationError

from portal.authentication.models import User
from portal.branch.models import Branch, Promotion
from portal.dish.models import Dish
from portal.order.models import Order, OrderStatus
from portal.restaurant.models import Restaurant
from portal.validators import Validators


class ValidateOrderAPIService:

    @classmethod
    def validate_data(
        cls, data: dict, branch_id: int, restaurant_id: int, user: User
    ):
        branch = Branch.objects.get(id=branch_id)
        cls.validate_delivery_type(restaurant_id, data['delivery_type'])
        cls.validate_dish_and_promotion(
            data.get('dishes'), data.get('promotions')
        )
        cls.validate_dishes(data.get('dishes', []), branch, restaurant_id)
        cls.validate_promotions(
            data.get('promotions', []), branch, restaurant_id
        )

    @staticmethod
    def validate_delivery_type(restaurant_id, delivery_type_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        if delivery_type_id not in restaurant.delivery_types.all():
            raise ValidationError({'delivery_type': 'Invalid delivery type.'})

    @staticmethod
    def validate_dish_and_promotion(dishes: list, promotions: list):
        if not (dishes or promotions):
            raise ValidationError({
                'non_field_errors': [
                    'There must be at least a dish or promotion selected.'
                ]
            })

    @classmethod
    def validate_dishes(
        cls, order_dishes: list, branch: Branch, restaurant_id: int
    ):
        for order_dish in order_dishes:
            cls.validate_dish(
                order_dish['dish'],
                order_dish['quantity'],
                branch,
                restaurant_id,
            )

    @classmethod
    def validate_promotions(
        cls, order_promotions: list, branch: Branch, restaurant_id: int
    ):
        for order_promotion in order_promotions:
            cls.validate_promotion(
                order_promotion['promotion'],
                order_promotion['quantity'],
                branch,
                restaurant_id,
            )

    @staticmethod
    def validate_dish(
        dish: Dish, quantity: int, branch: Branch, restaurant_id: int
    ):
        Validators.validate_restaurant_in_model(
            dish.category, restaurant_id, 'dish'
        )
        if not Validators.is_dish_available(branch, dish, quantity):
            raise ValidationError({
                'non_field_errors': [
                    f'At this moment the quantity {quantity} for dish'
                    f' {dish.name} is not available.'
                ]
            })

    @staticmethod
    def validate_promotion(
        promotion: Promotion, quantity: int, branch: Branch, restaurant_id: int
    ):
        Validators.validate_restaurant_in_model(
            promotion, restaurant_id, 'promotion',
        )
        if promotion.finish_date:
            Validators.validate_promotion_date(promotion)
        Validators.is_promotion_available(branch, promotion, quantity)

    @staticmethod
    def validate_next_status(order: Order, status: OrderStatus):
        if order.status != status.previous_status:
            raise ValidationError({
                'status': [
                    f'Order with status {order.status.name} cannot pass '
                    f'to status {status.name}'
                ]
            })

    @staticmethod
    def validate_client(user: User):
        if type(user) is AnonymousUser:
            raise ValidationError({
                "detail": "Authentication credentials were not provided."
            })

    @staticmethod
    def validate_stock(stock):
        if stock < 0:
            raise ValidationError({
                'non_field_errors': [
                    'There was a problem with the dishes availability.'
                ]
            })
