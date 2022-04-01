from rest_framework import status
from rest_framework.response import Response

from branch.models import Branch
from branch.serializers.branch import BranchSerializer


class BranchAPIService:

    @classmethod
    def create(
        cls, serializer: BranchSerializer, restaurant_id: int
    ) -> Response:
        branch = Branch(
            restaurant_id=restaurant_id,
            address=serializer.validated_data['address'],
            phone_number=serializer.validated_data['phone_number'],
            front_picture=serializer.validated_data['front_picture'],
        )
        branch.save()
        data = BranchSerializer(branch).data
        return Response(data, status=status.HTTP_201_CREATED)
