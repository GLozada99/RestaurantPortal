from rest_framework import serializers

from portal.dish.models import DishCategory


class DishCategorySerializer(serializers.ModelSerializer):
    """Serializer for DishCategory."""

    class Meta:
        model = DishCategory
        fields = (
            'id',
            'name',
        )
