from rest_framework import generics

from dish.models import Ingredient
from dish.serializers.ingredient import IngredientSerializer
from dish.services.ingredient import IngredientAPIService


class IngredientAPIView(generics.ListCreateAPIView):
    """View to list and create Ingredients."""

    serializer_class = IngredientSerializer
    # permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Ingredient.objects.filter(restaurant__id=restaurant_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return IngredientAPIService.create(
            serializer, self.kwargs.get('restaurant_id')
        )


class IngredientAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Ingredients."""

    serializer_class = IngredientSerializer
    # permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Ingredient.objects.filter(restaurant__id=restaurant_id)
