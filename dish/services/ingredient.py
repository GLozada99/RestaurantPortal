from rest_framework import status
from rest_framework.response import Response

from dish.models import Ingredient
from dish.serializers.ingredient import IngredientSerializer
from portal.validators import Validators


class IngredientAPIService:

    @classmethod
    def create(
        cls, serializer: IngredientSerializer, restaurant_id
    ) -> Response:
        cls.validate_restaurant(
            serializer.validated_data['name'], restaurant_id
        )
        serializer.save(restaurant_id=restaurant_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_restaurant(name, restaurant_id):
        Validators.validate_unique(
            Ingredient, name=name, restaurant_id=restaurant_id
        )
