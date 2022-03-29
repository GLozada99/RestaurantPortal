from rest_framework import serializers

from authentication.models import Role


class BasicUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'level')
