from rest_framework import generics

from dish.models import DishCategory
from dish.serializers.dish_category import (
    DetailedDishCategorySerializer,
    DishCategorySerializer,
)


class DishCategoryAPIView(generics.ListCreateAPIView):
    """View to list and create DishCategory."""

    serializer_class = DishCategorySerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DishCategorySerializer
        return DetailedDishCategorySerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return DishCategory.objects.filter(restaurant__id=restaurant_id)


class DishCategoryAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete DishCategory."""

    serializer_class = DishCategorySerializer

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return DishCategorySerializer
        return DetailedDishCategorySerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return DishCategory.objects.filter(restaurant__id=restaurant_id)
