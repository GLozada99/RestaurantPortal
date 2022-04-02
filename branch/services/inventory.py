from rest_framework import status
from rest_framework.response import Response

from branch.models import Inventory
from branch.serializers.inventory import InventorySerializer
from portal.validators import Validators


class InventoryAPIService:

    @classmethod
    def create(
        cls, serializer: InventorySerializer, branch_id
    ) -> Response:
        cls.validate_branch(
            branch_id, serializer.validated_data['ingredient']
        )
        serializer.save(branch_id=branch_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_branch(branch_id, ingredient_id):
        Validators.validate_unique(
            Inventory, branch=branch_id, ingredient=ingredient_id
        )
