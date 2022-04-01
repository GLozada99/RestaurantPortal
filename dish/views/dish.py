from rest_framework import generics

from dish.models import Dish
from dish.serializers.dish import DetailedDishSerializer, DishSerializer
from dish.services import DishAPIService


class DishAPIView(generics.ListCreateAPIView):
    """View to list and create Dish."""

    serializer_class = DishSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DishSerializer
        return DetailedDishSerializer

    def get_queryset(self):
        dish_category_id = self.kwargs['dish_category_id']
        return Dish.objects.filter(category__id=dish_category_id)

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return DishAPIService.create(serializer)


class DishAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Dish."""

    serializer_class = DishSerializer

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return DishSerializer
        return DetailedDishSerializer

    def get_queryset(self):
        dish_category_id = self.kwargs['dish_category_id']
        return Dish.objects.filter(category__id=dish_category_id)
