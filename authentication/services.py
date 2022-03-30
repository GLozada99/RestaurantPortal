from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

from authentication.models import Role
from authentication.serializers import UserSerializer
from portal.settings import CLIENT_LEVEL, PORTAL_MANAGER_LEVEL

User = get_user_model()


class UserAPIService:

    @staticmethod
    def create(serializer: UserSerializer) -> Response:
        user = User(
            username=serializer.validated_data['username'],
            role=serializer.validated_data['role'],
        )
        try:
            email = serializer.validated_data['email']
            user.email = email
        except KeyError:
            pass
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @classmethod
    def create_client(cls, serializer: UserSerializer) -> Response:
        serializer.validated_data['role'] = Role.objects.filter(
            level=CLIENT_LEVEL
        )
        return cls.create(serializer)

    @classmethod
    def create_portal_manager(cls, serializer: UserSerializer) -> Response:
        serializer.validated_data['role'] = Role.objects.filter(
            level=PORTAL_MANAGER_LEVEL
        )
        return cls.create(serializer)
