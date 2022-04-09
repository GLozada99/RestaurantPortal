from rest_framework import generics, status
from rest_framework.response import Response

from portal.authentication.permissions import (
    HasCurrentBranch,
    IsBranchManager,
    IsClient,
    IsEmployee,
)
from portal.order.handlers import OrderAPIHandler
from portal.order.models import Order
from portal.order.serializers.order import (
    CreateOrderSerializer,
    DetailedOrderSerializer,
    StatusOrderSerializer,
)


class OrderAPIView(generics.ListCreateAPIView):
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
            self.permission_classes = [IsClient]
        else:
            self.permission_classes = [
                (IsBranchManager | IsEmployee) & HasCurrentBranch
            ]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        data = OrderAPIHandler.handle(
            request, kwargs.get('restaurant_id'), kwargs.get('branch_id'),
        )
        return Response(data, status=status.HTTP_201_CREATED)


class OrderAPIDetailView(generics.RetrieveUpdateAPIView):
    """View to create Order."""

    def get_serializer_class(self):
        if self.request.method in {'PUT', 'PATCH'}:
            return StatusOrderSerializer
        return DetailedOrderSerializer

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        return Order.objects.filter(branch_id=branch_id)

    def get_permissions(self):
        if self.request.method in {'PUT', 'PATCH'}:
            self.permission_classes = [IsClient]
        else:
            self.permission_classes = [
                (IsBranchManager | IsEmployee) & HasCurrentBranch
            ]
        return super().get_permissions()
