
from rest_framework import generics

from portal.authentication.models import EmployeeProfile
from portal.authentication.permissions import (
    HasCurrentBranch,
    HasCurrentRestaurant,
    IsBranchManager,
    IsRestaurantManager,
)
from portal.authentication.serializers.employee_profile import \
    BranchProfileSerializer
from portal.authentication.serializers.user import UserSerializer
from portal.authentication.services import UserAPIService
from portal.mixins import CheckRestaurantBranchAccordingMixin
from portal.settings import EMPLOYEE_LEVEL


class EmployeeAPIView(
        CheckRestaurantBranchAccordingMixin, generics.ListCreateAPIView):
    """View to list and create Branch Employees."""

    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant) |
                          (IsBranchManager & HasCurrentBranch)]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserSerializer
        return BranchProfileSerializer

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        return EmployeeProfile.objects.filter(
            branch__id=branch_id,
            user__role__level=EMPLOYEE_LEVEL,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserAPIService.create_employee(
            serializer, self.kwargs.get('branch_id'),
        )


class EmployeeAPIDetailView(
        CheckRestaurantBranchAccordingMixin, generics.RetrieveDestroyAPIView):
    """View to retrieve and delete Branch Employees."""

    serializer_class = UserSerializer
    permission_classes = [(IsRestaurantManager & HasCurrentRestaurant) |
                          (IsBranchManager & HasCurrentBranch)]

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        return EmployeeProfile.objects.filter(
            branch__id=branch_id,
            user__role__level=EMPLOYEE_LEVEL,
        )
