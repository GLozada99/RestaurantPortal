from django.urls import path

from authentication.views import ClientAPIDetailView, ClientAPIView

app_name = 'authentication'
urlpatterns = [
    path('', ClientAPIView.as_view(), name='client-list'),
    path('<pk>/', ClientAPIDetailView.as_view(), name='client-detail'),
]
