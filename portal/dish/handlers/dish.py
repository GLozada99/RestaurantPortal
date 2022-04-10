from portal.dish.serializers.dish import (
    CreateDishSerializer,
    IngredientsDishSerializer,
    ReadDishSerializer,
)
from portal.dish.services.dish import DishAPIService, AvailableDishesAPIService


class DishAPIHandler:

    @classmethod
    def handle(cls, request, restaurant_id, category_id):
        serializer = CreateDishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return IngredientsDishSerializer(DishAPIService.create(
            serializer.validated_data,
            restaurant_id,
            category_id,
        )).data

    @staticmethod
    def get_available_dishes_category_branch(category_id: int, branch_id: int):
        available_dishes = AvailableDishesAPIService.get_available_dishes(
            category_id, branch_id,
        )
        return ReadDishSerializer(data=available_dishes, many=True).data
