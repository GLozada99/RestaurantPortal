from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response

from dish.models import Dish, DishIngredient
from dish.serializers.dish import DishSerializer
from portal.validators import Validators


class DishAPIService:

    @classmethod
    @atomic
    def create(cls, serializer: DishSerializer, category_id: int) -> Response:
        ingredients_data = serializer.validated_data.pop('ingredients')
        cls.validate_data(
            serializer.validated_data['name'], category_id, ingredients_data
        )
        serializer.save(category_id=category_id)
        cls.create_dish_ingredients(serializer, ingredients_data)
        cls.update_response_data(serializer, ingredients_data)
        return Response(
            DishSerializer(serializer.validated_data).data,
            status=status.HTTP_201_CREATED
        )

    @staticmethod
    def create_dish_ingredients(serializer: DishSerializer, ingredients_data):
        dish_ingredients = [
            DishIngredient(
                dish_id=serializer.data['id'],
                ingredient_id=dish_ingredient['ingredient'].id,
                quantity=dish_ingredient['quantity'],
                unit=dish_ingredient['unit'],
            ) for dish_ingredient in ingredients_data
        ]
        DishIngredient.objects.bulk_create(dish_ingredients)

    @staticmethod
    def update_response_data(serializer: DishSerializer, ingredients_data):
        serializer.validated_data['ingredients'] = ingredients_data
        serializer.validated_data['id'] = serializer.data['id']

    @classmethod
    def validate_data(cls, name, category_id, dish_ingredients):
        Validators.validate_unique(
            Dish, name=name, category_id=category_id,
        )
        Validators.validate_unique_id_in_list(
            dish_ingredients, 'ingredient', 'dish'
        )
