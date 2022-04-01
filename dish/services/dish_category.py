from rest_framework import status
from rest_framework.response import Response

from dish.serializers.dish_category import DishCategorySerializer


class DishCategoryAPIService:

    @classmethod
    def create(
        cls, serializer: DishCategorySerializer, restaurant_id
    ) -> Response:
        serializer.save(restaurant_id=restaurant_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
