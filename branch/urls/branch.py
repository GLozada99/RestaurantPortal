from django.urls import path, include

from branch.views.branch import BranchAPIDetailView, BranchAPIView

app_name = 'branch'
urlpatterns = [
    path('', BranchAPIView.as_view(), name='branch-list'),
    path(
        '<pk>/',
        BranchAPIDetailView.as_view(),
        name='branch-detail'
    ),
    path(
        '<branch_id>/inventory/',
        include('branch.urls.inventory', namespace='inventory')
    ),
]
