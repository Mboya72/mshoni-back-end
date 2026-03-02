from django.contrib import admin
from django.urls import path, include  # <--- Make sure 'path' and 'include' are here
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # Assuming your app is named 'api'
] 

# This serves media files (images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)