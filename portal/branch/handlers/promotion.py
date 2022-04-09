from portal.branch.serializers.promotion import (
    PromotionSerializer,
    DetailedPromotionSerializer,
)
from portal.branch.services.promotion import PromotionAPIService


class PromotionAPIHandler:

    @classmethod
    def handle(cls, request, restaurant_id):
        serializer = PromotionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return DetailedPromotionSerializer(PromotionAPIService.create(
            serializer.validated_data, restaurant_id
        )).data
