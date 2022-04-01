from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from dish.models import Dish, DishIngredient
from dish.serializers.dish import DishSerializer
from portal.validators import Validators


class DishAPIService:

    @classmethod
    def create(cls, serializer: DishSerializer, category_id: int) -> Response:
        Validators.validate_unique(
            Dish, name=serializer.validated_data['name'],
            category_id=category_id,
        )
        dish = Dish(
            name=serializer.validated_data['name'],
            price=serializer.validated_data['price'],
            description=serializer.validated_data['description'],
            category_id=category_id,
        )
        dish.save()
        ingredients_data = serializer.validated_data['ingredients']

        dish_ingredients = [
            DishIngredient(
                dish_id=dish.id,
                ingredient_id=data['ingredient'].id,
                quantity=data['quantity'],
                unit=data['unit'],
            ) for data in ingredients_data
        ]
        cls.validate_dish_ingredients(dish_ingredients)
        DishIngredient.objects.bulk_create(dish_ingredients)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_dish_ingredients(dish_ingredients):
        ingredients = []
        for dish_ingredient in dish_ingredients:
            if dish_ingredient.ingredient_id in ingredients:
                raise ValidationError({
                    'non_field_errors':
                        ['The fields ingredient, dish must make a unique set.']
                })
            ingredients.append(dish_ingredient.ingredient_id)
