from portal.dish.serializers.ingredient import IngredientSerializer
from portal.dish.services.ingredient import IngredientAPIService


class IngredientAPIHandler:

    @classmethod
    def handle(cls, request, restaurant_id):
        serializer = IngredientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return IngredientSerializer(IngredientAPIService.create(
            serializer.validated_data,
            restaurant_id,
        )).data
