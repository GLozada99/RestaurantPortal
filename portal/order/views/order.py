from rest_framework import generics

from portal.authentication.permissions import (
    HasCurrentBranch,
    IsBranchManager,
    IsClient,
    IsEmployee,
)
from portal.order.models import Order
from portal.order.serializers.order import (
    CreateOrderSerializer,
    DetailedOrderSerializer,
    StatusOrderSerializer,
)


class OrderAPIView(generics.CreateAPIView):
    """View to create Order."""

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return DetailedOrderSerializer

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        return Order.objects.filter(branch_id=branch_id)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsClient]
        return [(IsBranchManager | IsEmployee) & HasCurrentBranch]


class OrderAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to create Order."""

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return StatusOrderSerializer
        return DetailedOrderSerializer

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        return Order.objects.filter(branch_id=branch_id)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsClient]
        return [(IsBranchManager | IsEmployee) & HasCurrentBranch]
