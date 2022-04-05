from django.urls import path
from django.views.generic import TemplateView

from third_party_auth.views.google import GoogleSocialAuthView

app_name = 'google'
urlpatterns = [
    path('', GoogleSocialAuthView.as_view()),
    path('login/', TemplateView.as_view(
        template_name='third_party_auth/google.html'))
]
