from rest_framework import generics

from branch.models import Inventory
from branch.serializers.inventory import (DetailedInventorySerializer,
                                          InventorySerializer, )
from branch.services.inventory import InventoryAPIService


class InventoryAPIView(generics.ListCreateAPIView):
    """View to list and create Inventories."""
    # permission_classes = [(IsBranchManager & HasCurrentBranch)]
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InventorySerializer
        return DetailedInventorySerializer

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        return Inventory.objects.filter(branch_id=branch_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return InventoryAPIService.create(
            serializer,
            int(self.kwargs.get('restaurant_id')),
            self.kwargs.get('branch_id')
        )


class InventoryAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update and delete Inventory."""

    # permission_classes = [(IsBranchManager & HasCurrentBranch)]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return InventorySerializer
        return DetailedInventorySerializer

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        return Inventory.objects.filter(branch_id=branch_id)
