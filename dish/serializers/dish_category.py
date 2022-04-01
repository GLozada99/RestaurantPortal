from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from dish.models import DishCategory
from restaurant.serializers.restaurant import RestaurantSerializer


class DishCategorySerializer(serializers.ModelSerializer):
    """Serializer for DishCategory."""

    class Meta:
        model = DishCategory
        fields = ('id', 'name', 'restaurant')

        validators = [
            UniqueTogetherValidator(
                queryset=DishCategory.objects.all(),
                fields=['name', 'restaurant']
            )
        ]


class DetailedDishCategorySerializer(serializers.ModelSerializer):
    """Detailed Serializer for DishCategory."""
    restaurant = RestaurantSerializer()

    class Meta:
        model = DishCategory
        fields = ('id', 'name', 'restaurant')
