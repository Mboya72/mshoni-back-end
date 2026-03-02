from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: JsonResponse({'message': 'Mshoni API running!'})),
    path('api/v1/users/', include('api.users.urls')),
    path('api/v1/projects/', include('api.projects.urls')),
    path('api/v1/marketplace/', include('api.marketplace.urls')),
    path('api/v1/payments/', include('api.payments.urls')),
]