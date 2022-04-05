from rest_framework import generics

from authentication.permissions import (
    HasCurrentRestaurant,
    IsRestaurantManager,
)
from dish.models import Dish
from dish.serializers.dish import DetailedDishSerializer, DishSerializer
from dish.services.dish import DishAPIService
from portal.mixins import CheckRestaurantDishCategoryAccordingMixin


class DishAPIView(
    CheckRestaurantDishCategoryAccordingMixin, generics.ListCreateAPIView
):
    """View to list and create Dish."""

    serializer_class = DishSerializer
    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DishSerializer
        return DetailedDishSerializer

    def get_queryset(self):
        dish_category_id = self.kwargs.get('dish_category_id')
        return Dish.objects.filter(category__id=dish_category_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return DishAPIService.create(
            serializer,
            kwargs.get('dish_category_id'),
            int(kwargs.get('restaurant_id'))
        )


class DishAPIDetailView(
    CheckRestaurantDishCategoryAccordingMixin,
    generics.RetrieveDestroyAPIView
):
    """View to retrieve, update and delete Dish."""

    serializer_class = DishSerializer
    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return DishSerializer
        return DetailedDishSerializer

    def get_queryset(self):
        dish_category_id = self.kwargs.get('dish_category_id')
        return Dish.objects.filter(category__id=dish_category_id)
