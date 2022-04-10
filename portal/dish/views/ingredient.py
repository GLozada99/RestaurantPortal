from rest_framework import generics, status
from rest_framework.response import Response

from portal.authentication.permissions import (
    HasCurrentRestaurant,
    IsRestaurantManager,
)
from portal.dish.handlers.ingredient import IngredientAPIHandler
from portal.dish.models import Ingredient
from portal.dish.serializers.ingredient import IngredientSerializer


class IngredientAPIView(generics.ListCreateAPIView):
    """View to list and create Ingredients."""

    serializer_class = IngredientSerializer
    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Ingredient.objects.filter(restaurant_id=restaurant_id)

    def post(self, request, *args, **kwargs):
        data = IngredientAPIHandler.handle(
            request, kwargs.get('restaurant_id'),
        )
        return Response(data, status=status.HTTP_201_CREATED)


class IngredientAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Ingredients."""

    serializer_class = IngredientSerializer
    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Ingredient.objects.filter(restaurant_id=restaurant_id)
