from portal.branch.serializers.branch import CreateBranchSerializer
from portal.branch.services.branch import BranchAPIService


class BranchAPIHandler:

    @classmethod
    def handle(cls, request, restaurant_id):
        serializer = CreateBranchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return CreateBranchSerializer(BranchAPIService.create(
            serializer.validated_data,
            restaurant_id,
        )).data
