from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, BidViewSet, MarketplaceStatsView # Ensure StatsView is imported

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'bids', BidViewSet, basename='bids') # Added Bids

urlpatterns = [
    # Custom endpoints should usually come BEFORE router.urls if there is a conflict
    path('stats/', MarketplaceStatsView.as_view(), name='marketplace-stats'),
    path('', include(router.urls)),
]