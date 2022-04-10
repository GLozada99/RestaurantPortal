from portal.order.serializers.order import (
    CreateOrderSerializer,
    ReadOrderSerializer,
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
