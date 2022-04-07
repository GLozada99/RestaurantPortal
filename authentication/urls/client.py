from django.urls import path

from authentication.views.client import ClientAPIDetailView, ClientAPIView

app_name = 'client'
urlpatterns = [
    path('', ClientAPIView.as_view(), name='client-list'),
    path('<int:pk>/', ClientAPIDetailView.as_view(), name='client-detail'),
]
