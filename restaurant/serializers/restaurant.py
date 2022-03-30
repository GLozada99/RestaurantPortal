from rest_framework import serializers

from restaurant.models import Restaurant
from restaurant.serializers.delivery_type import DeliveryTypeSerializer
from restaurant.serializers.food_type import FoodTypeSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for Restaurant."""

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'food_type',
            'active_branches',
            'active_administrators',
            'is_active',
            'delivery_types'
        )


class DetailedRestaurantSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Restaurant."""

    food_type = FoodTypeSerializer()
    delivery_types = DeliveryTypeSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'food_type',
            'active_branches',
            'active_administrators',
            'is_active',
            'delivery_types'
        )
