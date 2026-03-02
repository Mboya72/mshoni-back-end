from django.urls import path
from .views import TestUsersView

urlpatterns = [
    path('test/', TestUsersView.as_view(), name='test-users'),
]