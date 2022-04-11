from django.urls import path

from portal.branch.views.promotion import (PromotionAPIDetailView,
                                           PromotionAPIView, )

app_name = 'branch'
urlpatterns = [
    path('', PromotionAPIView.as_view(), name='promotion-list'),
    path(
        '<int:pk>/',
        PromotionAPIDetailView.as_view(),
        name='promotion-detail',
    ),
]
