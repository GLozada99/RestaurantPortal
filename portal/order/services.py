from django.db.transaction import atomic
from rest_framework.serializers import ValidationError

from portal.authentication.models import User
from portal.branch.models import Branch
from portal.order.serializers.order import CreateOrderSerializer
from portal.validators import Validators


class OrderAPIService:

    @classmethod
    @atomic
    def create(
        cls, serializer: CreateOrderSerializer, restaurant_id, branch_id,
        user: User,
    ):
        ValidateOrderAPIService.validate_data(
            serializer.validated_data, branch_id, restaurant_id,
        )


class ValidateOrderAPIService():

    @classmethod
    def validate_data(cls, data, branch_id, restaurant_id):
        branch = Branch.objects.get(id=branch_id)
        cls.validate_dish_and_promotion(
            data.get('dishes'), data.get('promotions')
        )
        cls.validate_dishes(data.get('dishes'), branch, restaurant_id)
        cls.validate_promotions(data.get('promotions'), branch, restaurant_id)

    @staticmethod
    def validate_dish_and_promotion(dishes, promotions):
        if not (dishes or promotions):
            raise ValidationError({
                'non_field_errors': [
                    'There must be a dish or a promotion selected.'
                ]
            })

    @classmethod
    def validate_dishes(cls, order_dishes, branch: Branch, restaurant_id):
        if not order_dishes:
            return
        for order_dish in order_dishes:
            cls.validate_dish(
                order_dish['dish'],
                order_dish['quantity'],
                branch,
                restaurant_id,
            )

    @classmethod
    def validate_promotions(
        cls, order_promotions, branch: Branch, restaurant_id
    ):
        if not order_promotions:
            return
        for order_promotion in order_promotions:
            cls.validate_promotion(
                order_promotion['promotion'],
                order_promotion['quantity'],
                branch,
                restaurant_id,
            )

    @staticmethod
    def validate_dish(dish, quantity, branch: Branch, restaurant_id):
        Validators.validate_restaurant_in_model(
            dish.category, restaurant_id, 'dish'
        )
        if not Validators.is_dish_available(branch, dish, quantity):
            raise ValidationError({
                'non_field_errors': [
                    f'At this moment the dish {dish.name} is not available.'
                ]
            })

    @staticmethod
    def validate_promotion(promotion, quantity, branch: Branch, restaurant_id):
        Validators.validate_restaurant_in_model(
            promotion, restaurant_id, 'promotion'
        )
        if not Validators.is_promotion_available(
            branch, promotion, quantity,
        ):
            raise ValidationError({
                'non_field_errors': [
                    f'At this moment the promotion {promotion.name} is '
                    'not available.'
                ]
            })
