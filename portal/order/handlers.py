from portal.order.serializers.order import (
    CreateOrderSerializer,
    ReadOrderSerializer, StatusOrderSerializer,
)
from portal.order.services.order import OrderAPIService


class OrderAPIHandler:

    @classmethod
    def handle(cls, request, restaurant_id, branch_id):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return ReadOrderSerializer(OrderAPIService.create(
            serializer.validated_data,
            restaurant_id,
            branch_id,
            request.user,
        )).data

    @classmethod
    def update_status(
        cls, request, order_id: int
    ):
        serializer = StatusOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return StatusOrderSerializer(OrderAPIService.set_status(
            serializer.validated_data,
            order_id,
        )).data
