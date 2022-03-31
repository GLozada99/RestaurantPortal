from rest_framework import generics

from dish.models import Ingredient
from dish.serializers.ingredient import IngredientSerializer


class IngredientAPIView(generics.ListCreateAPIView):
    """View to list and create Ingredients."""

    queryset = Ingredient.objects.all().order_by('id')
    serializer_class = IngredientSerializer


class IngredientAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Ingredients."""

    queryset = Ingredient.objects.all().order_by('id')
    serializer_class = IngredientSerializer
