from rest_framework import serializers

from portal.restaurant.models import DeliveryType


class DeliveryTypeSerializer(serializers.ModelSerializer):
    """Serializer for DeliveryType."""

    class Meta:
        model = DeliveryType
        fields = (
            'id',
            'name',
        )
