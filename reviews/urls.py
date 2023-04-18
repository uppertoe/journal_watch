from django.urls import path, include
from .views import ReviewDetailView, ReviewListView

urlpatterns = [
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('review/<slug:slug>', ReviewDetailView.as_view(), name='review-detail'),
]