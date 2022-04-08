from rest_framework import generics

from portal.authentication.serializers.user import (PasswordChangeSerializer,
                                                    )
from portal.authentication.services import UserAPIService
from portal.mixins import CheckRestaurantBranchAccordingMixin


class PasswordAPIView(
        CheckRestaurantBranchAccordingMixin, generics.GenericAPIView):
    """View to change User password."""
    serializer_class = PasswordChangeSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return UserAPIService.change_password(serializer)
