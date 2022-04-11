from rest_framework import generics

from portal.authentication.permissions import (
    HasCurrentRestaurant,
    IsRestaurantManager,
)
from portal.dish.models import DishCategory
from portal.dish.serializers.dish_category import DishCategorySerializer
from portal.dish.services.dish_category import DishCategoryAPIService


class DishCategoryAPIView(generics.ListCreateAPIView):
    """View to list and create DishCategory."""

    serializer_class = DishCategorySerializer
    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return DishCategory.objects.filter(restaurant_id=restaurant_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return DishCategoryAPIService.create(
            serializer, self.kwargs.get('restaurant_id'),
        )


class DishCategoryAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete DishCategory."""

    serializer_class = DishCategorySerializer
    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return DishCategory.objects.filter(restaurant_id=restaurant_id)
