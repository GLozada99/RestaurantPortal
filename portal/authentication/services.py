from secrets import token_hex
from typing import Optional

from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from portal import settings
from portal.authentication.models import EmployeeProfile, Role
from portal.authentication.serializers.user import UserSerializer
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

    @classmethod
    @atomic
    def create(cls, serializer: UserSerializer, role_id: int) -> Response:
        user = None
        error = ''
        try:
            user = cls.make_user(
                serializer.validated_data['username'],
                serializer.validated_data['email'],
                role_id,
            )
        except ValueError as e:
            error = str(e)

        if user:
            response_data = {
                'data': UserSerializer(user).data,
                'status': status.HTTP_201_CREATED,
            }
            cls.send_password_change_email(user)
        else:
            response_data = {
                'data': {'message': error},
                'status': status.HTTP_400_BAD_REQUEST,
            }

        return Response(**response_data)

    @classmethod
    def create_profile(
        cls,
        user_id: int,
        restaurant_id: int = None,
        branch_id: int = None,
    ) -> EmployeeProfile:
        profile = EmployeeProfile(
            user_id=user_id, restaurant_id=restaurant_id, branch_id=branch_id,
        )
        profile.save()
        return profile

    @classmethod
    def create_client(cls, serializer: UserSerializer) -> Response:
        role_id = Role.objects.get(level=CLIENT_LEVEL).id
        return cls.create(serializer, role_id)

    @classmethod
    def create_portal_manager(cls, serializer: UserSerializer) -> Response:
        role_id = Role.objects.get(level=PORTAL_MANAGER_LEVEL).id
        return cls.create(serializer, role_id)

    @classmethod
    @atomic
    def create_employee(
        cls, serializer: UserSerializer, branch_id: int
    ) -> Response:
        role_id = Role.objects.get(level=EMPLOYEE_LEVEL).id
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
        Validators.validate_create_new_branch_manager(branch_id)
        role_id = Role.objects.get(level=BRANCH_MANAGER_LEVEL).id
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
        Validators.validate_create_new_restaurant_manager(restaurant_id)
        role_id = Role.objects.get(
            level=RESTAURANT_MANAGER_LEVEL,
        ).id
        user_data = cls.create(serializer, role_id).data
        user_id = user_data['id']
        profile = cls.create_profile(user_id, restaurant_id=restaurant_id)
        user_data.update({'restaurant_id': profile.restaurant.id})
        return Response(user_data, status=status.HTTP_201_CREATED)

    @classmethod
    def change_password(cls, serializer):
        user = cls.validate_user(serializer)
        cls.set_new_password(user, serializer)
        return Response(
            data={
                'message': 'Password changed successfully.'
            }, status=status.HTTP_202_ACCEPTED,
        )

    @classmethod
    def set_new_password(cls, user, serializer):
        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.change_password_token = None
        user.save()

    @classmethod
    def validate_user(cls, serializer):
        token = serializer.validated_data['change_password_token']
        email = serializer.validated_data['email']
        user = cls.get_user(email, token)
        return user

    @staticmethod
    def get_user(email, token):
        try:
            return User.objects.get(email=email, change_password_token=token)
        except User.DoesNotExist as e:
            raise ValidationError({
                'non_field_errors': [
                    'Could not validate email or token'
                ]
            }) from e

    @staticmethod
    def make_user(username: str, email: str, role_id: int):
        user = User.objects.create_user(
            username=username,
            password=token_hex(),
            email=email,
            role=Role.objects.get(pk=role_id),
            change_password_token=token_hex()
        )
        return user

    @classmethod
    def set_password_change_token(cls, serializer):
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except User.DoesNotExist as e:
            raise ValidationError({
                'email': 'User with this email does not exists',
            }) from e
        cls.validate_user_provider(user)

        user.change_password_token = token_hex()
        user.save()
        cls.send_password_change_email(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def send_password_change_email(user: User):
        subject = 'Password reset'
        message = ('This is your token to reset your password: '
                   f'{user.change_password_token}\n'
                   f'Please access {settings.EMAIL_PASSWORD_CHANGE_LINK} to '
                   f'change your password')
        user.email_user(subject, message)

    @staticmethod
    def validate_user_provider(user: User):
        if user.authentication_provider != 'portal':
            raise ValidationError({
                'non_field_errors': [
                    f'User with {user.authentication_provider} provider is '
                    f'not allowed to change its password'
                ]
            })


class UserPermissionService:

    @classmethod
    def get_restaurant_id(cls, user: User) -> Optional[int]:
        profile = EmployeeProfile.objects.get(user=user)
        return profile.restaurant.id if profile else None

    @classmethod
    def get_branch_id(cls, user: User) -> Optional[int]:
        profile = EmployeeProfile.objects.get(user=user)
        return profile.branch.id if profile else None


class UserEmailService:
    pass
