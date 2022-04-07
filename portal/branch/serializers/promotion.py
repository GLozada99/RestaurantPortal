from rest_framework import serializers

from portal.branch.models import Promotion
from portal.branch.serializers.branch import ShortBranchSerializer
from portal.branch.serializers.combo import (ComboSerializer,
                                             DetailedComboSerializer, )
from portal.validators import Validators


class PromotionSerializer(serializers.ModelSerializer):
    """Serializer for Promotion."""

    dishes = ComboSerializer(many=True)

    class Meta:
        model = Promotion
        fields = (
            'id',
            'name',
            'price',
            'branches',
            'dishes',
        )

    def validate_price(self, value):
        return Validators.validate_greater_than_zero(value)


class DetailedPromotionSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Promotion."""

    branches = ShortBranchSerializer(many=True)
    dishes = DetailedComboSerializer(many=True, source='combo_set')

    class Meta:
        model = Promotion
        fields = (
            'id',
            'name',
            'price',
            'branches',
            'dishes',
        )