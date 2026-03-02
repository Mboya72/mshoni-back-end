from django.urls import path
from .views import TestPaymentsView

urlpatterns = [
    path("test/", TestPaymentsView.as_view(), name="payments-test"),
]