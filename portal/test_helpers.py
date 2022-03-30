from functools import wraps

from rest_framework.reverse import reverse

from authentication.serializers import UserSerializer
from authentication.services import UserAPIService

user_data = {
    'username': 'UserTest',
    'password': 'root'
}


def get_portal_manager_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        serializer = UserSerializer(data=user_data)
        UserAPIService.create_portal_manager(serializer)
        self = args[0]
        token_url = reverse('auth:obtain-token')
        token = self.client.post(
            token_url, user_data, format='json'
        ).data['token']
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
        ).data['token']
        return f(*args, **kwargs, token=token)
    return wrapper
