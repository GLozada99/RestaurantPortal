from rest_framework import generics

from portal.authentication.permissions import (
    HasCurrentRestaurant,
    IsRestaurantManager,
    ReadOnly,
)
from portal.dish.models import Dish
from portal.dish.serializers.dish import (CreateDishSerializer,
                                          ReadDishSerializer, )
from portal.dish.services.dish import DishAPIService
from portal.mixins import (
    CheckRestaurantBranchAccordingMixin,
    CheckRestaurantDishCategoryAccordingMixin,
)


class DishAPIView(
    CheckRestaurantDishCategoryAccordingMixin, generics.ListCreateAPIView
):
    """View to list and create Dish."""

    serializer_class = CreateDishSerializer
    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateDishSerializer
        return ReadDishSerializer

    def get_queryset(self):
        dish_category_id = self.kwargs.get('dish_category_id')
        return Dish.objects.filter(category_id=dish_category_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return DishAPIService.create(
            serializer,
            kwargs.get('dish_category_id'),
            kwargs.get('restaurant_id'),
        )


class DishAPIDetailView(
    CheckRestaurantDishCategoryAccordingMixin,
    generics.RetrieveDestroyAPIView
):
    """View to retrieve, update and delete Dish."""

    serializer_class = CreateDishSerializer
    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant)]

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return CreateDishSerializer
        return ReadDishSerializer

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
        return DishAPIService.get_available_dishes_category_branch(
            dish_category_id, branch_id,
        )
