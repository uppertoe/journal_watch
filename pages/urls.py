from django.urls import path, include

from .views import Index

urlpatterns = [
    path('test/', Index.as_view(), name='index')
]