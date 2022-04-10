from rest_framework import generics, status
from rest_framework.response import Response

from portal.authentication.permissions import HasCurrentBranch, IsBranchManager
from portal.branch.handlers.inventory import InventoryAPIHandler
from portal.branch.models import Inventory
from portal.branch.serializers.inventory import (CreateInventorySerializer,
                                                 ReadInventorySerializer, )
from portal.mixins import CheckRestaurantBranchAccordingMixin


class InventoryAPIView(
    CheckRestaurantBranchAccordingMixin, generics.ListCreateAPIView
):
    """View to list and create Inventories."""

    permission_classes = [(IsBranchManager & HasCurrentBranch)]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateInventorySerializer
        return ReadInventorySerializer

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        return Inventory.objects.filter(branch_id=branch_id)

    def post(self, request, *args, **kwargs):
        data = InventoryAPIHandler.handle(
            request, kwargs.get('restaurant_id'), kwargs.get('branch_id'),
        )
        return Response(data, status=status.HTTP_201_CREATED)


class InventoryAPIDetailView(
    CheckRestaurantBranchAccordingMixin,
    generics.RetrieveUpdateDestroyAPIView
):

    """View to retrieve, update and delete Inventory."""

    permission_classes = [(IsBranchManager & HasCurrentBranch)]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CreateInventorySerializer
        return ReadInventorySerializer

    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        return Inventory.objects.filter(branch_id=branch_id)
