from functools import wraps

from rest_framework.reverse import reverse

from portal.authentication.serializers.user import UserSerializer
from portal.authentication.services import UserAPIService
from portal.branch.models import Branch
from portal.restaurant.models import Restaurant

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
