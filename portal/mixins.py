from django.http import JsonResponse
from rest_framework import status

from portal.branch.models import Branch
from portal.dish.models import DishCategory


class CheckRestaurantBranchAccordingMixin(object):

    @staticmethod
    def are_restaurant_branch_according(
        restaurant_id: int, branch_id: int
    ):
        branch = Branch.objects.filter(pk=branch_id).first()
        if branch:
            return branch.restaurant_id == restaurant_id
        return False

    def dispatch(self, request, *args, **kwargs):
        branch_id = self.kwargs.get('branch_id')
        restaurant_id = self.kwargs.get('restaurant_id')
        according = self.are_restaurant_branch_according(
            restaurant_id, branch_id
        )
        if not according:
            return JsonResponse(
                {'detail': 'Not found.'},
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
        dish_category = DishCategory.objects.filter(
            pk=dish_category_id
        ).first()
        if dish_category:
            return dish_category.restaurant_id == restaurant_id
        return False

    def dispatch(self, request, *args, **kwargs):
        dish_category_id = self.kwargs.get('dish_category_id')
        restaurant_id = self.kwargs.get('restaurant_id')
        according = self.are_restaurant_dish_category_according(
            restaurant_id, dish_category_id
        )
        if not according:
            return JsonResponse(
                {'detail': 'Not found.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super(CheckRestaurantDishCategoryAccordingMixin, self).dispatch(
            request, *args, **kwargs
        )
