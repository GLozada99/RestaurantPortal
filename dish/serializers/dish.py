from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from dish.models import Dish
from dish.serializers.dish_category import DishCategorySerializer
from dish.serializers.dish_ingredient import DishIngredientSerializer
from portal.validators import Validators


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

        validators = [
            UniqueTogetherValidator(
                queryset=Dish.objects.all(),
                fields=['name', 'category']
            )
        ]

    def validate_price(self, value):
        return Validators.validate_greater_than_zero(value)

    def validate_ingredients(self, value):
        return Validators.validate_list(value)


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
