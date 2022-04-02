from functools import wraps

from rest_framework.reverse import reverse

from authentication.serializers.user import UserSerializer
from authentication.services import UserAPIService

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
        token_url = reverse('auth:auth')
        token = self.client.post(
            token_url, user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper


def get_restaurant_manager_token(f):
    """This decorator only works if there's at least one restaurant created"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        serializer = UserSerializer(data=user_data)
        restaurant_id = 1
        UserAPIService.create_restaurant_manager(serializer, restaurant_id)
        self = args[0]
        token_url = reverse('auth:auth')
        token = self.client.post(
            token_url, user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper


def get_employee_token(f):
    """This decorator only works if there's at least one branch created"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        serializer = UserSerializer(data=user_data)
        branch_id = 1
        UserAPIService.create_restaurant_manager(serializer, branch_id)
        self = args[0]
        token_url = reverse('auth:auth')
        token = self.client.post(
            token_url, user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper


def get_branch_manager_token(f):
    """This decorator only works if there's at least one restaurant created"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        serializer = UserSerializer(data=user_data)
        branch_id = 1
        UserAPIService.create_branch_manager(serializer, branch_id)
        self = args[0]
        token_url = reverse('auth:auth')
        token = self.client.post(
            token_url, user_data, format='json'
        ).data['access']
        return f(*args, **kwargs, token=token)
    return wrapper
