from rest_framework import generics, permissions
from .models import Ticket
from .serializers import TicketSerializer

# 1. View for creating a ticket (Customer/Tailor/Seller)
class TicketCreateView(generics.CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the creator to the logged-in user
        serializer.save(creator=self.request.user)

# 2. View for listing tickets (Customer sees their own, Staff sees all)
class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()  # Support/Admin sees everything
        return Ticket.objects.filter(creator=user)  # Users only see their own tickets

# 3. View for seeing/updating a specific ticket (Dispute resolution)
class TicketDetailView(generics.RetrieveUpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]