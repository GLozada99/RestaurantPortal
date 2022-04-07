from rest_framework import serializers

from portal.dish.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
        )
