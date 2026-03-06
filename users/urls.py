from django.urls import path
from .views import RegisterView, UserDetailView, LoginView, GoogleLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'), # This fixes your 404!
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('google/', GoogleLoginView.as_view(), name='google-login'),
]