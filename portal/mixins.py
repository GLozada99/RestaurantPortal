from django.http import HttpResponse
from rest_framework import status

from branch.models import Branch


class CheckRestaurantBranchAccordingMixin(object):

    @staticmethod
    def are_restaurant_branch_according(
            restaurant_id: int, branch_id: int):

        branch = Branch.objects.get(pk=branch_id)
        if branch.restaurant_id != restaurant_id:
            return True

    def dispatch(self, request, *args, **kwargs):
        branch_id = int(self.kwargs.get('branch_id'))
        restaurant_id = int(self.kwargs.get('restaurant_id'))
        result = self.are_restaurant_branch_according(branch_id,
                                                      restaurant_id)
        if result:
            return HttpResponse(
                f'The branch with id {branch_id} does  not '
                f'belong to the restaurant with id {restaurant_id}',
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super(CheckRestaurantBranchAccordingMixin, self).dispatch(
            request,
            *args,
            **kwargs
        )
