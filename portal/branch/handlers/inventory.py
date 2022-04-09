from portal.branch.serializers.inventory import (DetailedInventorySerializer,
                                                 InventorySerializer, )
from portal.branch.services.inventory import InventoryAPIService


class InventoryAPIHandler:

    @classmethod
    def handle(cls, request, restaurant_id, branch_id):
        serializer = InventorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return DetailedInventorySerializer(InventoryAPIService.create(
            serializer.validated_data,
            restaurant_id,
            branch_id,
        )).data
