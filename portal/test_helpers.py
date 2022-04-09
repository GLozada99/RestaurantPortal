from functools import wraps

from rest_framework.reverse import reverse

from portal.authentication.models import User
from portal.authentication.serializers.user import UserSerializer
from portal.authentication.services import UserAPIService
from portal.branch.models import Branch
from portal.restaurant.models import Restaurant

create_user_data = {
    'username': 'UserTest',
    'email': 'test@mail.com'
}
auth_user_data = {
    'username': create_user_data['username'],
    'password': 'TestPassword',
}


def _set_password(email: str):
    user = User.objects.get(email=email)
    user.set_password(auth_user_data['password'])
    user.save()


def get_portal_manager_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        serializer = UserSerializer(data=create_user_data)
        serializer.is_valid()
        UserAPIService.create_portal_manager(serializer)
        _set_password(serializer.validated_data['email'])
        self = args[0]
        token_url = reverse('auth:obtain-token')
        token = self.client.post(
            token_url, auth_user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper


def get_client_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        serializer = UserSerializer(data=create_user_data)
        serializer.is_valid()
        UserAPIService.create_client(serializer)
        _set_password(serializer.validated_data['email'])
        self = args[0]
        token_url = reverse('auth:obtain-token')
        token = self.client.post(
            token_url, auth_user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper


def get_restaurant_manager_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        serializer = UserSerializer(data=create_user_data)
        serializer.is_valid(raise_exception=True)
        UserAPIService.create_restaurant_manager(
            serializer,
            Restaurant.objects.all().first().id
        )
        _set_password(serializer.validated_data['email'])
        self = args[0]
        token_url = reverse('auth:obtain-token')
        token = self.client.post(
            token_url, auth_user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper


def get_employee_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        serializer = UserSerializer(data=create_user_data)
        serializer.is_valid(raise_exception=True)
        UserAPIService.create_employee(
            serializer,
            Branch.objects.all().first().id
        )
        _set_password(serializer.validated_data['email'])
        self = args[0]
        token_url = reverse('auth:obtain-token')
        token = self.client.post(
            token_url, auth_user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper


def get_branch_manager_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        serializer = UserSerializer(data=create_user_data)
        serializer.is_valid(raise_exception=True)
        UserAPIService.create_branch_manager(
            serializer,
            Branch.objects.all().first().id
        )
        _set_password(serializer.validated_data['email'])
        self = args[0]
        token_url = reverse('auth:obtain-token')
        token = self.client.post(
            token_url, auth_user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper
