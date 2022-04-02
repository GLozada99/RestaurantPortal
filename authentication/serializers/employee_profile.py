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
        )


class BranchEmployeeSerializer(EmployeeProfileSerializer):
    """Serializer for EmployeeProfile to be used for Employees and Branch
    Managers"""
    class Meta:
        model = EmployeeProfile
        fields = EmployeeProfileSerializer.Meta.fields + ('branch',)


class RestaurantManagerSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeProfile to be used for Restaurant Managers"""
    class Meta:
        model = EmployeeProfile
        fields = EmployeeProfileSerializer.Meta.fields + ('restaurant',)
