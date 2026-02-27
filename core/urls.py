from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Flutter will POST email/password here to get tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Flutter will use this to stay logged in without re-entering password
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]