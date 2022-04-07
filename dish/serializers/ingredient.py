from rest_framework import serializers

from dish.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
        )
