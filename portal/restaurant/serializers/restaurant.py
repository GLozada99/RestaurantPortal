from rest_framework import serializers
from rest_framework.serializers import ValidationError

from portal.restaurant.models import Restaurant
from portal.restaurant.serializers.delivery_type import DeliveryTypeSerializer
from portal.restaurant.serializers.food_type import FoodTypeSerializer
from portal.validators import Validators


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
            'delivery_types',
        )

    def validate_active_branches(self, value):
        Validators.validate_greater_than_zero(value)
        instance = self.instance
        if instance and Validators.validate_active_branches(
            instance, value,
        ):
            raise ValidationError(
                'This field cannot be less than the number of branches',
            )
        return value

    def validate_active_administrators(self, value):
        Validators.validate_greater_than_zero(value)
        instance = self.instance
        if instance and Validators.validate_active_restaurant_managers(
            instance, value,
        ):
            raise ValidationError(
                'This field cannot be less than the number of '
                'restaurant administrators.',
            )
        return value


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
            'delivery_types',
        )
