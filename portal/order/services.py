from django.db.transaction import atomic
from rest_framework.serializers import ValidationError

from portal import settings
from portal.authentication.models import User
from portal.branch.models import Branch, Promotion
from portal.dish.models import Dish
from portal.order.models import Order, OrderDish, OrderStatus
from portal.order.serializers.order import CreateOrderSerializer
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
        order = Order(
            client=user,
            delivery_type_id=serializer.validated_data['delivery_type'],
            status=OrderStatus.objects.get(
                position_order=settings.CREATED_POSITION_ORDER),
            branch_id=branch_id,
            address=serializer.validated_data['address'],
            price=cls.calculate_total_price(
                serializer.validated_data['dishes'],
                serializer.validated_data['promotions'],
            )
        )
        order.save()
        cls.add_dishes_to_order(serializer.validated_data['dishes'], order)
        cls.add_promotions_to_order(
            serializer.validated_data['promotions'], order,
        )

    @classmethod
    def calculate_total_price(cls, dishes_data: list, promotions_data: list):
        return (cls.calculate_dishes_price(dishes_data) +
                cls.calculate_promotions_price(promotions_data))

    @staticmethod
    def calculate_dishes_price(dishes_data: list):
        dishes_ids = [dish_data['dish'] for dish_data in dishes_data]
        dishes_prices = Dish.objects.filter(
            pk__in=dishes_ids,
        ).values_list('price')
        return sum(
            (
                (dish_price * dish_data['quantity'])
                for dish_data, dish_price in zip(
                 dishes_data, dishes_prices)
            )
        )

    @staticmethod
    def calculate_promotions_price(promotions_data: list):
        promotions_ids = [promotion_data['promotion'] for promotion_data in
                          promotions_data]
        promotions_prices = Promotion.objects.filter(
            pk__in=promotions_ids,
        ).values_list('price')
        return sum(
            (
                (promotion_price * promotion_data['quantity'])
                for promotion_data, promotion_price in zip(
                 promotions_data, promotions_prices)
            )
        )

    @staticmethod
    def add_dishes_to_order(dishes_data: dict, order: Order):
        for dish_data in dishes_data:
            OrderDish.objects.create(
                order=order,
                dish_id=dish_data['dish'],
                quantity=dish_data['quantity'],
            )

    @staticmethod
    def add_promotions_to_order(promotions_data: dict, order: Order):
        for promotion_data in promotions_data:
            OrderDish.objects.create(
                order=order,
                promotion_id=promotion_data['promotion'],
                quantity=promotion_data['quantity'],
            )


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
        cls.validate_dishes(data.get('dishes'), branch, restaurant_id)
        cls.validate_promotions(data.get('promotions'), branch, restaurant_id)
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
        cls, order_promotions: list, branch: Branch, restaurant_id: int
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
