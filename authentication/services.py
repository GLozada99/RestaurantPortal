from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class UserAPIService():

    @staticmethod
    def create(serializer):
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
