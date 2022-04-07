from rest_framework import status
from rest_framework.response import Response

from portal.branch.serializers.branch import BranchSerializer
from portal.validators import Validators


class BranchAPIService:

    @classmethod
    def create(cls, serializer: BranchSerializer, restaurant_id) -> Response:
        Validators.validate_create_new_branch(restaurant_id)
        serializer.save(restaurant_id=restaurant_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
