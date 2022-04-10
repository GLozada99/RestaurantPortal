from rest_framework import generics, status
from rest_framework.response import Response

from portal.authentication.permissions import (
    HasCurrentRestaurant,
    IsRestaurantManager,
    ReadOnly,
)
from portal.dish.handlers.dish import DishAPIHandler
from portal.dish.models import Dish
from portal.dish.serializers.dish import (
    CreateDishSerializer,
    ReadDishSerializer,
)
from portal.mixins import (
    CheckRestaurantBranchAccordingMixin,
    CheckRestaurantDishCategoryAccordingMixin,
)


class DishAPIView(
    CheckRestaurantDishCategoryAccordingMixin, generics.ListCreateAPIView
):
    """View to list and create Dish."""

    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateDishSerializer
        return ReadDishSerializer

    def get_queryset(self):
        dish_category_id = self.kwargs.get('dish_category_id')
        return Dish.objects.filter(category_id=dish_category_id)

    def post(self, request, *args, **kwargs):
        data = DishAPIHandler.handle(
            request,
            kwargs.get('restaurant_id'),
            kwargs.get('dish_category_id'),
        )
        return Response(data, status=status.HTTP_201_CREATED)


class DishAPIDetailView(
    CheckRestaurantDishCategoryAccordingMixin,
    generics.RetrieveDestroyAPIView
):
    """View to retrieve, update and delete Dish."""

    serializer_class = ReadDishSerializer
    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_queryset(self):
        dish_category_id = self.kwargs.get('dish_category_id')
        return Dish.objects.filter(category_id=dish_category_id)


class DishBranchCategoryAvailableAPIView(
    CheckRestaurantBranchAccordingMixin,
    CheckRestaurantDishCategoryAccordingMixin,
    generics.GenericAPIView,
):
    """View to get Dishes available in specific Branch and Dish Category."""

    serializer_class = ReadDishSerializer
    permission_classes = [ReadOnly]

    def get(self, request, *args, **kwargs):
        branch_id = self.kwargs.get('branch_id')
        dish_category_id = self.kwargs.get('dish_category_id')
        return DishAPIHandler.get_available_dishes_category_branch(
            dish_category_id, branch_id,
        )
