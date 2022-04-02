from rest_framework import status
from rest_framework.response import Response

from dish.models import Ingredient
from dish.serializers.ingredient import IngredientSerializer
from portal.validators import Validators


class IngredientAPIService:

    @classmethod
    def create(
        cls, serializer: IngredientSerializer, restaurant
    ) -> Response:
        cls.validate_restaurant(
            serializer.validated_data['name'], restaurant
        )
        serializer.save(restaurant_id=restaurant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_restaurant(name, restaurant):
        Validators.validate_unique(
            Ingredient, name=name, restaurant=restaurant
        )
