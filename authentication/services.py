from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

from authentication.models import EmployeeProfile, Role
from authentication.serializers.user import UserSerializer
from portal.settings import (BRANCH_MANAGER_LEVEL, CLIENT_LEVEL,
                             EMPLOYEE_LEVEL,
                             PORTAL_MANAGER_LEVEL, RESTAURANT_MANAGER_LEVEL, )

User = get_user_model()


class UserAPIService:

    @staticmethod
    def create(serializer: UserSerializer, role_id: int) -> Response:
        user = User(
            username=serializer.validated_data['username'],
            role_id=role_id,
        )
        try:
            email = serializer.validated_data['email']
            user.email = email
        except KeyError:
            pass
        user.set_password(serializer.validated_data['password'])
        user.save()
        final_data = UserSerializer(user).data
        return Response(final_data, status=status.HTTP_201_CREATED)

    @classmethod
    def create_profile(
            cls,
            user_id: int,
            restaurant_id: int = None,
            branch_id: int = None) -> EmployeeProfile:
        profile = EmployeeProfile(
            user_id=user_id,
            restaurant_id=restaurant_id,
            branch_id=branch_id
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


class EmployeeProfileAPIService:
    @classmethod
    def create_user(
            cls,
            serializer: UserSerializer,
            role_id: int) -> dict:
        user_data = {
            'username': serializer.validated_data['username'],
            'password': serializer.validated_data['password'],
            'email': serializer.validated_data.get('email'),
        }
        user_serializer = UserSerializer(data=user_data)
        response = UserAPIService.create(user_serializer)
        return response.data



    @classmethod
    def create_employee(
            cls, serializer: EmployeeProfileSerializer) -> Response:
        employee_id = Role.objects.filter(level=EMPLOYEE_LEVEL).first().id
        user_data = cls.create_user(serializer, employee_id)
        user_id = user_data['id']
        profile = cls.create_profile(serializer, user_id)

        final_data = BranchEmployeeSerializer(profile).data
        return Response(final_data, status=status.HTTP_201_CREATED)

    @classmethod
    def create_branch_manager(
            cls, serializer: EmployeeProfileSerializer) -> Response:
        branch_manager_id = Role.objects.filter(
            level=BRANCH_MANAGER_LEVEL).first().id
        user_data = cls.create_user(serializer, branch_manager_id)
        user_id = user_data['id']
        profile = cls.create_profile(serializer, user_id)

        final_data = BranchEmployeeSerializer(profile).data
        return Response(final_data, status=status.HTTP_201_CREATED)

    @classmethod
    def create_restaurant_manager(
            cls,
            serializer: EmployeeProfileSerializer,
            restaurant_id: int) -> Response:

        restaurant_manager_id = Role.objects.filter(
            level=RESTAURANT_MANAGER_LEVEL).first().id
        user_data = cls.create_user(serializer, restaurant_manager_id)

        user_id = user_data['id']
        profile = cls.create_profile(
            serializer,
            user_id,
            restaurant_id=restaurant_id
        )

        final_data = RestaurantManagerSerializer(profile).data
        return Response(final_data, status=status.HTTP_201_CREATED)
