from rest_framework import generics

from branch.models import Branch
from branch.serializers.branch import BranchSerializer


class BranchAPIView(generics.ListCreateAPIView):
    """View to list and create Branch."""

    serializer_class = BranchSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Branch.objects.filter(restaurant__id=restaurant_id)


class BranchAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Branch."""

    serializer_class = BranchSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return Branch.objects.filter(restaurant__id=restaurant_id)
