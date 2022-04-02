
from rest_framework import generics

from authentication.models import EmployeeProfile
from authentication.serializers.user import UserSerializer
from authentication.services import UserAPIService
from portal.settings import BRANCH_MANAGER_LEVEL


class RestaurantManagerAPIView(generics.ListCreateAPIView):
    """View to list and create Branch Managers."""

    serializer_class = UserSerializer

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        return EmployeeProfile.objects.filter(
            branch__id=branch_id,
            user__role__level=BRANCH_MANAGER_LEVEL
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserAPIService.create_branch_manager(
            serializer, self.kwargs.get('branch_id')
        )


class RestaurantManagerAPIDetailView(generics.RetrieveDestroyAPIView):
    """View to retrieve and delete Branch Managers."""

    serializer_class = UserSerializer

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        return EmployeeProfile.objects.filter(
            branch__id=branch_id,
            user__role__level=BRANCH_MANAGER_LEVEL
        )
