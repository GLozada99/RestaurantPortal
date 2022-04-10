from portal.branch.serializers.branch import BranchSerializer
from portal.branch.services.branch import BranchAPIService


class BranchAPIHandler:

    @classmethod
    def handle(cls, request, restaurant_id):
        serializer = BranchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return BranchSerializer(BranchAPIService.create(
            serializer.validated_data,
            restaurant_id,
        )).data
