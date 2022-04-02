
from rest_framework import generics

from authentication.models import EmployeeProfile
from authentication.serializers.employee_profile import \
    RestaurantProfileSerializer
from authentication.serializers.user import UserSerializer
from authentication.services import UserAPIService
from portal.settings import RESTAURANT_MANAGER_LEVEL


class RestaurantManagerAPIView(generics.ListCreateAPIView):
    """View to list and create Restaurant Managers."""

    # permission_classes = [(IsRestaurantManager &
    # HasCurrentRestaurant) | IsPortalManager]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserSerializer
        return RestaurantProfileSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return EmployeeProfile.objects.filter(
            restaurant__id=restaurant_id,
            user__role__level=RESTAURANT_MANAGER_LEVEL
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserAPIService.create_restaurant_manager(
            serializer, self.kwargs.get('restaurant_id')
        )


class RestaurantManagerAPIDetailView(generics.RetrieveDestroyAPIView):
    """View to retrieve and delete Restaurant Managers."""

    serializer_class = UserSerializer
    # permission_classes = [(IsRestaurantManager &
    # HasCurrentRestaurant) | IsPortalManager]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return EmployeeProfile.objects.filter(
            restaurant__id=restaurant_id,
            user__role__level=RESTAURANT_MANAGER_LEVEL
        )
