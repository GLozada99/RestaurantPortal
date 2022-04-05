from django.urls import path

from third_party_auth.views.google import GoogleSocialAuthView

app_name = 'google'
urlpatterns = [
    path('', GoogleSocialAuthView.as_view()),
]
