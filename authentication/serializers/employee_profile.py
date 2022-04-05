from rest_framework import serializers

from authentication.models import EmployeeProfile
from authentication.serializers.user import UserSerializer


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
