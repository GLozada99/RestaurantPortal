from portal.branch.serializers.inventory import (CreateInventorySerializer,
                                                 ReadInventorySerializer, )
from portal.branch.services.inventory import InventoryAPIService


class InventoryAPIHandler:

    @classmethod
    def handle(cls, request, restaurant_id, branch_id):
        serializer = CreateInventorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return ReadInventorySerializer(InventoryAPIService.create(
            serializer.validated_data,
            restaurant_id,
            branch_id,
        )).data
