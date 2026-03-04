from rest_framework import generics, permissions
from .models import Project, ProjectUpdate
from .serializers import ProjectSerializer, ProjectUpdateSerializer

# List all projects for the logged-in tailor, or create a new one
class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # A tailor only sees their own projects; a customer sees projects assigned to them
        user = self.request.user
        if user.role == 'tailor':
            return Project.objects.filter(user=user)
        return Project.objects.filter(customer__user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Detailed view of a single project (to update status or delete)
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

# View to post a progress update (e.g., moving to "Sewing" or "First Fitting")
class ProjectUpdateCreateView(generics.CreateAPIView):
    serializer_class = ProjectUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]