from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token


class GoogleUserServices:
    @staticmethod
    def validate_token(token: str):
        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request())
            if 'accounts.google.com' in id_info['iss']:
                return id_info
        except GoogleAuthError:
            raise ValueError
