from rest_framework import generics, permissions
from .models import Ticket
from .serializers import TicketSerializer

class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff: # Admins see all tickets
            return Ticket.objects.all()
        # Users see tickets they created
        return Ticket.objects.filter(creator=user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)