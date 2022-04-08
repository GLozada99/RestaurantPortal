from django.urls import path

from portal.authentication.views.branch_manager import (
    BranchManagerAPIDetailView,
    BranchManagerAPIView,
)

app_name = 'authentication'
urlpatterns = [
    path('', BranchManagerAPIView.as_view(),
         name='branch-manager-list'),
    path(
        '<int:pk>/',
        BranchManagerAPIDetailView.as_view(),
        name='branch-manager-detail',
    ),
]
