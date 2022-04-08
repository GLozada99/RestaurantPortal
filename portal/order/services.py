from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from portal import settings
from portal.authentication.models import User
from portal.branch.models import Branch, Promotion
from portal.dish.models import Dish
from portal.order.models import OrderDish, OrderStatus
from portal.order.serializers.order import (
    CreateOrderSerializer,
    DetailedOrderSerializer,
)
from portal.validators import Validators


class OrderAPIService:

    @classmethod
    @atomic
    def create(
        cls, serializer: CreateOrderSerializer,
        restaurant_id: int, branch_id: int, user: User
    ):
        ValidateOrderAPIService.validate_data(
            serializer.validated_data, branch_id, restaurant_id, user,
        )
        dishes = serializer.validated_data.pop('dishes', [])
        promotions = serializer.validated_data.pop('promotions', [])
        serializer.save(
            client=user,
            status=OrderStatus.objects.get(
                position_order=settings.CREATED_POSITION_ORDER,
            ),
            branch_id=branch_id,
            total_cost=cls.calculate_total_price(dishes, promotions),
        )
        cls.add_dishes_to_order(dishes, serializer.data)
        cls.add_promotions_to_order(promotions, serializer.data)
        cls.update_response_data(serializer, dishes, promotions)
        return Response(
            DetailedOrderSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED,
        )

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
    def add_dishes_to_order(dishes_data: dict, order: dict):
        for dish_data in dishes_data:
            OrderDish.objects.create(
                order_id=order['id'],
                dish_id=dish_data['dish'].id,
                quantity=dish_data['quantity'],
            )

    @staticmethod
    def add_promotions_to_order(promotions_data: dict, order: dict):
        for promotion_data in promotions_data:
            OrderDish.objects.create(
                order_id=order['id'],
                promotion_id=promotion_data['promotion'].id,
                quantity=promotion_data['quantity'],
            )

    @staticmethod
    def update_response_data(
        serializer: CreateOrderSerializer, dishes: dict, promotions: dict
    ):
        serializer.validated_data['dishes'] = dishes
        serializer.validated_data['promotions'] = promotions
        serializer.validated_data['id'] = serializer.data['id']


class ValidateOrderAPIService:

    @classmethod
    def validate_data(
            cls, data: dict, branch_id: int,
            restaurant_id: int, user: User
    ):
        branch = Branch.objects.get(id=branch_id)
        cls.validate_dish_and_promotion(
            data.get('dishes'), data.get('promotions')
        )
        cls.validate_dishes(data.get('dishes', []), branch, restaurant_id)
        cls.validate_promotions(
            data.get('promotions', []), branch, restaurant_id
        )
        cls.validate_user_client(user)

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
            dish: Dish, quantity: int,
            branch: Branch, restaurant_id: int
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
            promotion: Promotion, quantity: int,
            branch: Branch, restaurant_id: int):
        Validators.validate_restaurant_in_model(
            promotion, restaurant_id, 'promotion'
        )
        if not Validators.is_promotion_available(
            branch, promotion, quantity,
        ):
            raise ValidationError({
                'non_field_errors': [
                    f'At this moment the quantity {quantity} for promotion '
                    f'{promotion.name} is not available.'
                ]
            })

    @staticmethod
    def validate_user_client(user: User):
        if user.role.level != settings.CLIENT_LEVEL:
            raise ValidationError({
                'non_field_errors': [
                    'Only clients can make orders'
                ]
            })
