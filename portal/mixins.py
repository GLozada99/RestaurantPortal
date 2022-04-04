from django.http import JsonResponse
from rest_framework import status

from branch.models import Branch
from dish.models import DishCategory


class CheckRestaurantBranchAccordingMixin(object):

    @staticmethod
    def are_restaurant_branch_according(
        restaurant_id: int, branch_id: int
    ):
        branch = Branch.objects.get(pk=branch_id)
        return branch.restaurant_id == restaurant_id

    def dispatch(self, request, *args, **kwargs):
        branch_id = int(self.kwargs.get('branch_id'))
        restaurant_id = int(self.kwargs.get('restaurant_id'))
        according = self.are_restaurant_branch_according(
            restaurant_id, branch_id
        )
        if not according:
            return JsonResponse(
                {
                    'detail':
                    f'The branch with id {branch_id} does not '
                    f'belong to the restaurant with id {restaurant_id}'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super(CheckRestaurantBranchAccordingMixin, self).dispatch(
            request, *args, **kwargs
        )


class CheckRestaurantDishCategoryAccordingMixin(object):

    @staticmethod
    def are_restaurant_dish_category_according(
        restaurant_id: int, dish_category_id: int
    ):
        dish_category = DishCategory.objects.get(pk=dish_category_id)
        return dish_category.restaurant_id == restaurant_id

    def dispatch(self, request, *args, **kwargs):
        dish_category_id = int(self.kwargs.get('dish_category_id'))
        restaurant_id = int(self.kwargs.get('restaurant_id'))
        according = self.are_restaurant_dish_category_according(
            restaurant_id, dish_category_id
        )
        if not according:
            return JsonResponse(
                {
                    'detail':
                    f'The dish category with id {dish_category_id} does not '
                    f'belong to the restaurant with id {restaurant_id}'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super(CheckRestaurantDishCategoryAccordingMixin, self).dispatch(
            request, *args, **kwargs
        )
