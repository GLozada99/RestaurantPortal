from rest_framework import generics

from authentication.permissions import (
    HasCurrentRestaurant,
    IsRestaurantManager,
)
from branch.models import Branch
from branch.serializers.branch import BranchSerializer
from branch.services.branch import BranchAPIService


class BranchAPIView(generics.ListCreateAPIView):
    """View to list and create Branch."""

    serializer_class = BranchSerializer
    permission_classes = [IsRestaurantManager & HasCurrentRestaurant]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Branch.objects.filter(restaurant__id=restaurant_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return BranchAPIService.create(
            serializer, self.kwargs.get('restaurant_id')
        )


class BranchAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Branch."""

    serializer_class = BranchSerializer
    permission_classes = [IsRestaurantManager & HasCurrentRestaurant]

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Branch.objects.filter(restaurant__id=restaurant_id)
