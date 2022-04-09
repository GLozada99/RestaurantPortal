from django.db.models import Model
from rest_framework.serializers import ValidationError

from portal.branch.models import Inventory
from portal.validators import Validators


class InventoryAPIService:

    @classmethod
    def create(
        cls, data: dict, restaurant_id: int, branch_id: int,
    ) -> Model:
        cls.validate_data(
            restaurant_id, branch_id, data['ingredient'],
        )
        inventory = cls.get_instance(data, branch_id)
        return inventory

    @classmethod
    def get_instance(cls, data: dict, branch_id: int) -> Inventory:
        inventory = Inventory(
            branch_id=branch_id,
            ingredient=data['ingredient'],
            stock=data['stock'],
            unit=data['unit'],
        )
        inventory.save()
        return inventory

    @classmethod
    def validate_data(cls, restaurant_id, branch_id, ingredient):
        cls.validate_branch(branch_id, ingredient)
        cls.validate_ingredient(restaurant_id, ingredient)

    @staticmethod
    def validate_ingredient(restaurant_id, ingredient):
        if ingredient.restaurant_id != restaurant_id:
            raise ValidationError({
                'ingredient': 'Invalid ingredient.',
            })

    @staticmethod
    def validate_branch(branch_id, ingredient):
        Validators.validate_unique(
            Inventory, branch=branch_id, ingredient=ingredient,
        )
