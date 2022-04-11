from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from portal.third_party_auth.handlers import GoogleSocialAuthHandler
from portal.third_party_auth.serializers.google import GoogleAuthSerializer


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleAuthSerializer

    def post(self, request):
        data = GoogleSocialAuthHandler.handle(request)
        return Response(data, status=status.HTTP_200_OK)
