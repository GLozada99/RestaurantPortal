from rest_framework import generics

from portal.authentication.permissions import (
    HasCurrentRestaurant,
    IsRestaurantManager,
)
from portal.branch.models import Branch
from portal.branch.serializers.branch import BranchSerializer
from portal.branch.services.branch import BranchAPIService


class BranchAPIView(generics.ListCreateAPIView):
    """View to list and create Branch."""

    serializer_class = BranchSerializer
    permission_classes = [IsRestaurantManager & HasCurrentRestaurant]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Branch.objects.filter(restaurant_id=restaurant_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return BranchAPIService.create(
            serializer, self.kwargs.get('restaurant_id'),
        )


class BranchAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Branch."""

    serializer_class = BranchSerializer
    permission_classes = [IsRestaurantManager & HasCurrentRestaurant]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Branch.objects.filter(restaurant_id=restaurant_id)
