from functools import wraps

from django.core.management import call_command
from rest_framework.reverse import reverse

from authentication.serializers.user import UserSerializer
from authentication.services import UserAPIService
from branch.models import Branch
from restaurant.models import Restaurant

user_data = {
    'username': 'UserTest',
    'password': 'root'
}


def get_portal_manager_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        serializer = UserSerializer(data=user_data)
        serializer.is_valid()
        UserAPIService.create_portal_manager(serializer)
        self = args[0]
        token_url = reverse('auth:obtain-token')
        token = self.client.post(
            token_url, user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper


def get_client_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        serializer = UserSerializer(data=user_data)
        UserAPIService.create_client(serializer)
        self = args[0]
        token_url = reverse('auth:obtain-token')
        token = self.client.post(
            token_url, user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper


def get_restaurant_manager_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        call_command('createrestaurants')
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        UserAPIService.create_restaurant_manager(
            serializer,
            Restaurant.objects.all().first().id
        )
        self = args[0]
        token_url = reverse('auth:obtain-token')
        token = self.client.post(
            token_url, user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper


def get_employee_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        call_command('createrestaurants')
        call_command('createbranches')
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        UserAPIService.create_employee(
            serializer,
            Branch.objects.all().first().id)
        self = args[0]
        token_url = reverse('auth:obtain-token')
        token = self.client.post(
            token_url, user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper


def get_branch_manager_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        call_command('createrestaurants')
        call_command('createbranches')
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        UserAPIService.create_branch_manager(
            serializer,
            Branch.objects.all().first().id
        )
        self = args[0]
        token_url = reverse('auth:obtain-token')
        token = self.client.post(
            token_url, user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper
