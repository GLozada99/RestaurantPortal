from rest_framework import generics

from portal.authentication.permissions import (
    HasCurrentRestaurant,
    IsRestaurantManager,
)
from portal.dish.models import Ingredient
from portal.dish.serializers.ingredient import IngredientSerializer
from portal.dish.services.ingredient import IngredientAPIService


class IngredientAPIView(generics.ListCreateAPIView):
    """View to list and create Ingredients."""

    serializer_class = IngredientSerializer
    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Ingredient.objects.filter(restaurant_id=restaurant_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return IngredientAPIService.create(
            serializer, self.kwargs.get('restaurant_id'),
        )


class IngredientAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Ingredients."""

    serializer_class = IngredientSerializer
    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Ingredient.objects.filter(restaurant_id=restaurant_id)
