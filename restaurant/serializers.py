from rest_framework import serializers

from restaurant.models import DeliveryType, FoodType, Restaurant


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


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for Restaurant"""

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'food_type', 'active_branches',
                  'active_administrators', 'is_active', 'delivery_types')


class DetailedRestaurantSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Restaurant"""
    food_type = FoodTypeSerializer()
    delivery_types = DeliveryTypeSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'food_type', 'active_branches',
                  'active_administrators', 'is_active', 'delivery_types')
