from rest_framework import serializers

from dish.models import DishIngredient
from dish.serializers.ingredient import IngredientSerializer
from portal.validators import Validators


class DishIngredientSerializer(serializers.ModelSerializer):
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


class DetailedDishIngredientSerializer(serializers.ModelSerializer):
    """Detailed Serializer for DishIngredient."""

    ingredient = IngredientSerializer()

    class Meta:
        model = DishIngredient
        fields = (
            'ingredient',
            'quantity',
            'unit',
        )
