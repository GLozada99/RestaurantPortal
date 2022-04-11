from rest_framework import serializers

from portal.dish.models import DishIngredient
from portal.dish.serializers.ingredient import IngredientSerializer
from portal.validators import Validators


class CreateDishIngredientSerializer(serializers.ModelSerializer):
    """Serializer for DishIngredient."""

    class Meta:
        model = DishIngredient
        fields = (
            'ingredient',
            'quantity',
            'unit',
        )

    def validate_quantity(self, value):
        return Validators.validate_greater_than_zero(value)


class ReadDishIngredientSerializer(serializers.ModelSerializer):
    """Detailed Serializer for DishIngredient."""

    ingredient = IngredientSerializer()

    class Meta:
        model = DishIngredient
        fields = (
            'ingredient',
            'quantity',
            'unit',
        )
