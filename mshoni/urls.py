"""
URL configuration for mshoni project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # 1. Django Admin
    path('admin/', admin.site.urls),

    # 2. Authentication (Custom App)
    # This points to your new authentication/urls.py which contains login and register
    path('api/auth/', include('authentication.urls')),
    
    # 3. Token Refresh (Keep this here so Flutter can refresh expired tokens)
    
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 4. Mshoni App APIs
    path('api/users/', include('users.urls')),          
    path('api/profiles/', include('profiles.urls')),    
    path('api/projects/', include('projects.urls')),    
    path('api/media/', include('media_file.urls')),     
    path('api/tickets/', include('tickets.urls')),      
]

# 5. Media & Static File Serving
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)