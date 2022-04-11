from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from portal.dish.models import Dish
from portal.dish.serializers.dish_ingredient import (
    CreateDishIngredientSerializer,
    ReadDishIngredientSerializer,
)
from portal.validators import Validators


class ShortDishSerializer(serializers.ModelSerializer):
    """Short Serializer for Dish."""

    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
        )


class CreateDishSerializer(serializers.ModelSerializer):
    """Serializer for Dish."""

    ingredients = CreateDishIngredientSerializer(many=True)
    picture = Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
            'price',
            'description',
            'ingredients',
            'picture',
        )

    def validate_price(self, value):
        return Validators.validate_greater_than_zero(value)

    def validate_ingredients(self, value):
        return Validators.validate_list(value)


class ReadDishSerializer(serializers.ModelSerializer):
    """Serializer for Dish."""

    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
            'price',
            'description',
            'picture',
        )


class IngredientsDishSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Dish with ingredients."""

    ingredients = ReadDishIngredientSerializer(
        many=True, source='dishingredient_set'
    )

    class Meta:
        model = Dish
        fields = (
            'id',
            'name',
            'price',
            'description',
            'ingredients',
        )
