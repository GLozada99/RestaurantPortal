from rest_framework import generics

from dish.models import DishCategory
from dish.serializers.dish_category import (DetailedDishCategorySerializer,
                                            DishCategorySerializer, )


class DishCategoryAPIView(generics.ListCreateAPIView):
    """View to list and create DishCategory."""

    queryset = DishCategory.objects.all().order_by('id')
    serializer_class = DishCategorySerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DishCategorySerializer
        return DetailedDishCategorySerializer


class DishCategoryAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete DishCategory."""

    queryset = DishCategory.objects.all().order_by('id')
    serializer_class = DishCategorySerializer

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return DishCategorySerializer
        return DetailedDishCategorySerializer
