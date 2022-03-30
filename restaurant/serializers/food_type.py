from rest_framework import serializers

from restaurant.models import FoodType


class FoodTypeSerializer(serializers.ModelSerializer):
    """Serializer for FoodType."""

    class Meta:
        model = FoodType
        fields = ('id', 'name')
