from rest_framework import serializers

from portal.branch.models import Inventory
from portal.dish.serializers.ingredient import IngredientSerializer
from portal.validators import Validators


class CreateInventorySerializer(serializers.ModelSerializer):
    """Serializer for Inventory."""

    class Meta:
        model = Inventory
        fields = (
            'id',
            'ingredient',
            'stock',
            'unit',
        )

    def validate_stock(self, value):
        return Validators.validate_greater_than_or_equal_to_zero(value)


class ReadInventorySerializer(serializers.ModelSerializer):
    """Detailed Serializer for Inventory."""

    ingredient = IngredientSerializer()

    class Meta:
        model = Inventory
        fields = (
            'id',
            'ingredient',
            'stock',
            'unit',
        )
