from django.urls import path

from branch.views.branch import BranchAPIDetailView, BranchAPIView

app_name = 'branch'
urlpatterns = [
    path('', BranchAPIView.as_view(), name='branch-list'),
    path(
        '<pk>/',
        BranchAPIDetailView.as_view(),
        name='branch-detail'
    ),
]
