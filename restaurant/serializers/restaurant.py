from rest_framework import serializers

from portal.validators import Validators
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
            'delivery_types'
        )

    def validate_active_branches(self, value):
        return Validators.validate_greater_than_zero(value)

    def validate_active_administrators(self, value):
        return Validators.validate_greater_than_zero(value)


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
