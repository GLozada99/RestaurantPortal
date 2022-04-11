from datetime import datetime

from rest_framework import serializers

from portal.branch.models import Promotion
from portal.branch.serializers.branch import ShortBranchSerializer
from portal.branch.serializers.combo import (
    CreateComboSerializer,
    ReadComboSerializer,
)
from portal.validators import Validators


class ShortPromotionSerializer(serializers.ModelSerializer):
    """Short Serializer for Promotion."""

    class Meta:
        model = Promotion
        fields = (
            'id',
            'name',
        )


class PromotionSerializer(serializers.ModelSerializer):
    """Serializer for Promotion."""

    dishes = CreateComboSerializer(many=True)

    class Meta:
        model = Promotion
        fields = (
            'id',
            'name',
            'price',
            'branches',
            'dishes',
            'start_date',
            'finish_date',
        )

    def validate_price(self, value):
        return Validators.validate_greater_than_zero(value)

    def validate_start_date(self, value):
        return Validators.validate_date(value)

    def validate_finish_date(self, value):
        print(self.initial_data)
        start_date = self.initial_data.get('start_date')
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if value < start_date:
            raise serializers.ValidationError(
                'Invalid date, cannot be less than the start date.'
            )
        return value


class DetailedPromotionSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Promotion."""

    branches = ShortBranchSerializer(many=True)
    dishes = ReadComboSerializer(many=True, source='combo_set')

    class Meta:
        model = Promotion
        fields = (
            'id',
            'name',
            'price',
            'branches',
            'dishes',
            'start_date',
            'finish_date',
        )
