from rest_framework import serializers

from dish.models import DishIngredient
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
