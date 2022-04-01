from rest_framework import status
from rest_framework.response import Response

from branch.serializers.branch import BranchSerializer


class BranchAPIService:

    @classmethod
    def create(cls, serializer: BranchSerializer, restaurant_id) -> Response:
        serializer.validated_data['restaurant_id'] = restaurant_id
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
