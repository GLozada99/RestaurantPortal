from rest_framework import status
from rest_framework.response import Response

from dish.models import Dish, DishIngredient
from dish.serializers.dish import DishSerializer


class DishAPIService:

    @staticmethod
    def create(serializer: DishSerializer) -> Response:
        dish = Dish(
            name=serializer.validated_data['name'],
            price=serializer.validated_data['price'],
            description=serializer.validated_data['description'],
            category=serializer.validated_data['category'],
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
        DishIngredient.objects.bulk_create(dish_ingredients)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
