from portal.third_party_auth.serializers.google import GoogleAuthSerializer
from portal.third_party_auth.services import (GeneralUserServices,
                                              GoogleUserServices, )


class GoogleSocialAuthHandler:

    @classmethod
    def handle(cls, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data['token']
        # GoogleUserServices.validate_google_id(data.get('aud'))
        user_data = GoogleUserServices.get_user_data(data)

        return GeneralUserServices.register_get_user(**user_data)
