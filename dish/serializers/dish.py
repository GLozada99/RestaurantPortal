from rest_framework import serializers

from dish.models import Dish
from dish.serializers.dish_category import DishCategorySerializer


class DishSerializer(serializers.ModelSerializer):
    """Serializer for Dish."""

    class Meta:
        model = Dish
        fields = ('id',
                  'name',
                  'price',
                  'description',
                  'category')


class DetailedDishSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Dish."""
    category = DishCategorySerializer()

    class Meta:
        model = Dish
        fields = ('id',
                  'name',
                  'price',
                  'description',
                  'category')
