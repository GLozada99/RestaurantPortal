from rest_framework import serializers

from dish.models import Dish
from dish.serializers.dish_ingredient import (
    DishIngredientSerializer,
    DetailedDishIngredientSerializer,
)
from portal.validators import Validators


class ShortDishSerializer(serializers.ModelSerializer):
    """Short Serializer for Dish."""

    class Meta:
        model = Dish
        fields = (
            'id',
            'name'
        )


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
            'ingredients'
        )

    def validate_price(self, value):
        return Validators.validate_greater_than_zero(value)

    def validate_ingredients(self, value):
        return Validators.validate_list(value)


class DetailedDishSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Dish."""

    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
            'price',
            'description',
        )


class DetailedDishWithIngredientsSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Dish with ingredients."""

    ingredients = DetailedDishIngredientSerializer(many=True)

    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
            'price',
            'description',
            'ingredients'
        )
