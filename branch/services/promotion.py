from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from branch.models import Combo
from branch.serializers.promotion import (
    PromotionSerializer,
    DetailedPromotionSerializer,
)
from portal.validators import Validators


class PromotionAPIService:

    @classmethod
    @atomic
    def create(
        cls, serializer: PromotionSerializer, restaurant_id
    ) -> Response:
        combos_data = serializer.validated_data.pop('dishes')
        cls.validate_data(
            restaurant_id, serializer.validated_data['branches'], combos_data
        )
        serializer.save(restaurant_id=restaurant_id)
        serializer.validated_data['dishes'] = combos_data
        combos = [
            Combo(
                promotion_id=serializer.data['id'],
                dish_id=combo['dish'].id,
                quantity=combo['quantity']
            ) for combo in combos_data
        ]
        Combo.objects.bulk_create(combos)
        return Response(
            DetailedPromotionSerializer(serializer.validated_data).data,
            status=status.HTTP_201_CREATED
        )

    @classmethod
    def validate_data(cls, restaurant_id, branches, combos):
        Validators.validate_unique_id_in_list(
            combos, 'dish', 'promotion'
        )
        cls.validate_branches(restaurant_id, branches)
        cls.validate_dishes(restaurant_id, combos)

    @staticmethod
    def validate_branches(restaurant_id, branches):
        for branch in branches:
            if branch.restaurant_id != restaurant_id:
                raise ValidationError({
                    'branches': 'Invalid branches.'
                })

    @staticmethod
    def validate_dishes(restaurant_id, combos):
        for combo in combos:
            if combo['dish'].category.restaurant_id != restaurant_id:
                raise ValidationError({
                    'dishes': 'Invalid dishes.'
                })
