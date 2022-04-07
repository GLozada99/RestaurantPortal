from rest_framework import status
from rest_framework.response import Response

from dish.models import DishCategory
from dish.serializers.dish_category import DishCategorySerializer
from portal.validators import Validators


class DishCategoryAPIService:

    @classmethod
    def create(
        cls, serializer: DishCategorySerializer, restaurant_id
    ) -> Response:
        cls.validate_restaurant(
            serializer.validated_data['name'], restaurant_id,
        )
        serializer.save(restaurant_id=restaurant_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_restaurant(name, restaurant_id):
        Validators.validate_unique(
            DishCategory, name=name, restaurant=restaurant_id,
        )
