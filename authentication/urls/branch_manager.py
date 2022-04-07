from django.urls import path

from authentication.views.branch_manager import (
    BranchManagerAPIDetailView,
    BranchManagerAPIView,
)

app_name = 'branch_manager'
urlpatterns = [
    path('', BranchManagerAPIView.as_view(),
         name='branch-manager-list'),
    path(
        '<int:pk>/',
        BranchManagerAPIDetailView.as_view(),
        name='branch-manager-detail',
    ),
]
