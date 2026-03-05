from django.urls import path
from .views import TicketCreateView, TicketListView, TicketDetailView

urlpatterns = [
    # For Customers to submit a new issue
    path('create/', TicketCreateView.as_view(), name='ticket-create'),
    
    # For Users to see their own history / Support to see all
    path('list/', TicketListView.as_view(), name='ticket-list'),
    
    # To view or update a specific dispute/ticket
    path('<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
]