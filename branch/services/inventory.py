from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from branch.models import Inventory
from branch.serializers.inventory import InventorySerializer
from portal.validators import Validators


class InventoryAPIService:

    @classmethod
    def create(
        cls, serializer: InventorySerializer, restaurant_id, branch_id
    ) -> Response:
        cls.validate_data(
            restaurant_id, branch_id, serializer.validated_data['ingredient']
        )
        serializer.save(branch_id=branch_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @classmethod
    def validate_data(cls, restaurant_id, branch_id, ingredient):
        cls.validate_branch(branch_id, ingredient)
        cls.validate_ingredient(restaurant_id, ingredient)

    @staticmethod
    def validate_ingredient(restaurant_id, ingredient):
        if ingredient.restaurant_id != restaurant_id:
            raise ValidationError({
                'ingredient': 'Invalid ingredient.'
            })

    @staticmethod
    def validate_branch(branch_id, ingredient):
        Validators.validate_unique(
            Inventory, branch=branch_id, ingredient=ingredient
        )
