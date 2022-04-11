from django.db.transaction import atomic
from rest_framework.serializers import ValidationError

from portal.branch.models import Combo, Promotion
from portal.validators import Validators


class PromotionAPIService:

    @classmethod
    @atomic
    def create(cls, data: dict, restaurant_id):
        combos_data = data.pop('dishes')
        branches_data = data.pop('branches')
        ValidatePromotionAPIService.validate_data(
            restaurant_id, branches_data, combos_data,
        )
        promotion = cls.get_instance(data, restaurant_id)
        cls.add_branches(promotion, branches_data)
        cls.create_combos(promotion, combos_data)
        return promotion

    @classmethod
    def get_instance(cls, data: dict, restaurant_id):
        promotion = Promotion(
            name=data['name'],
            price=data['price'],
            restaurant_id=restaurant_id,
            start_date=data['start_date'],
            finish_date=data.get('finish_date'),
        )
        promotion.save()
        return promotion

    @staticmethod
    def add_branches(promotion: Promotion, branches):
        promotion.branches.set(branches)
        promotion.save()

    @staticmethod
    def create_combos(promotion: Promotion, combos_data):
        combos = [
            Combo(
                promotion_id=promotion.id,
                dish_id=combo['dish'].id,
                quantity=combo['quantity'],
            ) for combo in combos_data
        ]
        Combo.objects.bulk_create(combos)


class ValidatePromotionAPIService:

    @classmethod
    def validate_data(cls, restaurant_id, branches, combos):
        Validators.validate_unique_id_in_list(
            combos, 'dish', 'promotion',
        )
        cls.validate_branches(restaurant_id, branches)
        cls.validate_dishes(restaurant_id, combos)

    @staticmethod
    def validate_branches(restaurant_id, branches):
        for branch in branches:
            if branch.restaurant_id != restaurant_id:
                raise ValidationError({
                    'branches': 'Invalid branches.',
                })

    @staticmethod
    def validate_dishes(restaurant_id, combos):
        for combo in combos:
            if combo['dish'].category.restaurant_id != restaurant_id:
                raise ValidationError({
                    'dishes': 'Invalid dishes.',
                })
