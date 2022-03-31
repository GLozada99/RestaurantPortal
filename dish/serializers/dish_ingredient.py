from rest_framework import serializers

from dish.models import DishIngredient


class DishIngredientSerializer(serializers.ModelSerializer):
    """Serializer for DishIngredient."""

    class Meta:
        model = DishIngredient
        fields = (
            'ingredient',
            'quantity',
            'unit',
        )
