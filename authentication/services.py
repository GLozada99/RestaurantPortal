from typing import Optional

from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response

from authentication.models import EmployeeProfile, Role
from authentication.serializers.user import UserSerializer
from portal.settings import (
    BRANCH_MANAGER_LEVEL,
    CLIENT_LEVEL,
    EMPLOYEE_LEVEL,
    PORTAL_MANAGER_LEVEL,
    RESTAURANT_MANAGER_LEVEL,
)
from portal.validators import Validators

User = get_user_model()


class UserAPIService:

    @staticmethod
    def create(serializer: UserSerializer, role_id: int) -> Response:
        user_data = {
            'username': serializer.validated_data['username'],
            'password': serializer.validated_data['password'],
            'role': Role.objects.get(pk=role_id),
        }
        try:
            user_data['email'] = serializer.validated_data['email']
        except KeyError:
            pass

        try:
            user = User.objects.create_user(**user_data)
            response_data = {
                'data': UserSerializer(user).data,
                'status': status.HTTP_201_CREATED
            }
        except ValueError as e:
            response_data = {
                'data': {'message': str(e)},
                'status': status.HTTP_400_BAD_REQUEST,
            }
        return Response(**response_data)

    @classmethod
    def create_profile(
        cls,
        user_id: int,
        restaurant_id: int = None,
        branch_id: int = None
    ) -> EmployeeProfile:
        profile = EmployeeProfile(
            user_id=user_id, restaurant_id=restaurant_id, branch_id=branch_id
        )
        profile.save()
        return profile

    @classmethod
    def create_client(cls, serializer: UserSerializer) -> Response:
        role_id = Role.objects.filter(level=CLIENT_LEVEL).first().id
        return cls.create(serializer, role_id)

    @classmethod
    def create_portal_manager(cls, serializer: UserSerializer) -> Response:
        role_id = Role.objects.filter(level=PORTAL_MANAGER_LEVEL).first().id
        return cls.create(serializer, role_id)

    @classmethod
    @atomic
    def create_employee(
        cls, serializer: UserSerializer, branch_id: int
    ) -> Response:
        role_id = Role.objects.filter(level=EMPLOYEE_LEVEL).first().id
        user_data = cls.create(serializer, role_id).data
        user_id = user_data['id']
        profile = cls.create_profile(user_id, branch_id=branch_id)
        user_data.update({'branch_id': profile.branch.id})
        return Response(user_data, status=status.HTTP_201_CREATED)

    @classmethod
    @atomic
    def create_branch_manager(
        cls, serializer: UserSerializer, branch_id: int
    ) -> Response:
        role_id = Role.objects.filter(level=BRANCH_MANAGER_LEVEL).first().id
        user_data = cls.create(serializer, role_id).data
        user_id = user_data['id']
        profile = cls.create_profile(user_id, branch_id=branch_id)
        user_data.update({'branch_id': profile.branch.id})
        return Response(user_data, status=status.HTTP_201_CREATED)

    @classmethod
    @atomic
    def create_restaurant_manager(
        cls, serializer: UserSerializer, restaurant_id: int
    ) -> Response:
        role_id = Role.objects.filter(
            level=RESTAURANT_MANAGER_LEVEL
        ).first().id
        Validators.validate_create_new_restaurant_manager(restaurant_id)
        user_data = cls.create(serializer, role_id).data
        user_id = user_data['id']
        profile = cls.create_profile(user_id, restaurant_id=restaurant_id)
        user_data.update({'restaurant_id': profile.restaurant.id})
        return Response(user_data, status=status.HTTP_201_CREATED)


class UserPermissionService:

    @classmethod
    def get_restaurant_id(cls, user: User) -> Optional[int]:
        profile = EmployeeProfile.objects.filter(user=user).first()
        return profile.restaurant.id if profile else None

    @classmethod
    def get_branch_id(cls, user: User) -> Optional[int]:
        profile = EmployeeProfile.objects.filter(user=user).first()
        return profile.branch.id if profile else None
