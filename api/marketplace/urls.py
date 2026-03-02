from django.urls import path
from .views import TestMarketplaceView

urlpatterns = [
    path("test/", TestMarketplaceView.as_view(), name="marketplace-test"),
]