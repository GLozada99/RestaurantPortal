from rest_framework import serializers

from dish.models import Dish
from dish.serializers.dish_category import DishCategorySerializer
from dish.serializers.dish_ingredient import DishIngredientSerializer


class DishSerializer(serializers.ModelSerializer):
    """Serializer for Dish."""

    ingredients = DishIngredientSerializer(many=True)

    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
            'price',
            'description',
            'category',
            'ingredients'
        )


class DetailedDishSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Dish."""
    category = DishCategorySerializer()

    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
            'price',
            'description',
            'category'
        )
