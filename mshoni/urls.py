"""
URL configuration for mshoni project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "Mshoni Backend is online", "version": "1.0.0"})

urlpatterns = [
    path('', health_check),
    # 1. Django Admin
    path('admin/', admin.site.urls),

    # 2. Authentication & Users
    path('api/auth/', include('authentication.urls')),
    path('api/users/', include('users.urls')),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 3. Mshoni Core App APIs
    path('api/inventory/', include('inventory.urls')),           
    path('api/profiles/', include('profiles.urls')),    
    path('api/projects/', include('projects.urls')),    
    path('api/media/', include('media_file.urls')),     
    path('api/tickets/', include('tickets.urls')),

    # 4. Marketplace & Chat (THE FIXES)
    path('api/marketplace/', include('marketplace.urls')), # Added Marketplace
    path('api/chat/', include('chat.urls')),               # Added Chat
]

# 5. Media & Static File Serving
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)