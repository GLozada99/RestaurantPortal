from django.urls import path

from portal.authentication.views.client import SignUpAPIView

app_name = 'authentication'
urlpatterns = [
    path('', SignUpAPIView.as_view(), name='sign-up'),
]
