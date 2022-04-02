from rest_framework import serializers

from authentication.models import EmployeeProfile
from authentication.serializers.user import UserSerializer


class EmployeeProfileSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeProfile"""
    user = UserSerializer()

    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
            'user',
            'restaurant',
            'branch',
        )
