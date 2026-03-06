from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, GoogleLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'), # Mapping for /api/users/login/
    path('google/', GoogleLoginView.as_view(), name='google_login'), # Mapping for /api/users/google/
    path('profile/', UserDetailView.as_view(), name='profile'),
]