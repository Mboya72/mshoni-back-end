from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, MeasurementViewSet, LookbookViewSet, MessageViewSet, 
    TagViewSet, NotificationViewSet, CustomerProfileViewSet, 
    JobViewSet, ProjectViewSet
)

# Initialize the router
router = DefaultRouter()

# Profile & Personal Data
router.register(r'measurements', MeasurementViewSet, basename='measurement')
router.register(r'customer-profiles', CustomerProfileViewSet, basename='customer-profile')

# Tailor Specific
router.register(r'lookbook', LookbookViewSet, basename='lookbook')
router.register(r'tags', TagViewSet, basename='tag')

# Jobs & Workflow
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'projects', ProjectViewSet, basename='project')

# Communication & Updates
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # Auth Endpoints
    path('register/', RegisterView.as_view(), name='register'),
    
    # JWT Auth (Recommended for your App)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Routes
    path('', include(router.urls)),
]