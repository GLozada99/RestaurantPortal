from rest_framework import serializers

from authentication.models import EmployeeProfile
from authentication.serializers.user import UserSerializer


class EmployeeProfileSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeProfile to be used for Employees and Branch
    Admins"""
    user = UserSerializer()

    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
            'user',
            'branch',
        )


class RestaurantAdminProfileSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeProfile to be used for Restaurant Admins"""
    user = UserSerializer()

    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
            'user',
            'restaurant',
        )
