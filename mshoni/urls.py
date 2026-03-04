"""
URL configuration for mshoni project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 1. Django Admin
    path('admin/', admin.site.urls),

    # 2. Authentication (JWT)
    # Flutter will hit these to log in and get new tokens
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 3. Mshoni App APIs
    path('api/users/', include('users.urls')),          # Profile management
    path('api/profiles/', include('profiles.urls')),    # Lookbooks and tailor details
    path('api/projects/', include('projects.urls')),    # Orders and fitting updates
    path('api/media/', include('media_file.urls')),     # Centralized image uploads
    path('api/tickets/', include('tickets.urls')),      # Support and disputes

]

# 4. Media & Static File Serving
# This allows you to view uploaded images in your browser during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)