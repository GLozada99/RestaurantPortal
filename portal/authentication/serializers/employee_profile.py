from rest_framework import serializers

from portal.authentication.models import EmployeeProfile
from portal.authentication.serializers.user import UserSerializer


class RestaurantProfileSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeProfile on Restaurant Managers"""
    user = UserSerializer()

    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
            'user',
            'restaurant',
        )


class BranchProfileSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeProfile on Branch Employees and Managers"""
    user = UserSerializer()

    class Meta:
        model = EmployeeProfile
        fields = (
            'id',
            'user',
            'branch',
        )
