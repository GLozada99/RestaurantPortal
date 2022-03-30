from rest_framework import serializers

from restaurant.models import DeliveryType, FoodType


class FoodTypeSerializer(serializers.ModelSerializer):
    """Serializer for FoodType"""

    class Meta:
        model = FoodType
        fields = ('id', 'name')


class DeliveryTypeSerializer(serializers.ModelSerializer):
    """Serializer for DeliveryType"""

    class Meta:
        model = DeliveryType
        fields = ('id', 'name')
