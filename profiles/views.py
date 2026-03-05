from rest_framework import generics, permissions
from .models import Project, ProjectUpdate
from .serializers import ProjectSerializer, ProjectUpdateSerializer

# List all projects for the logged-in user
class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Accessing role via the Profile model
        if hasattr(user, 'profile') and user.profile.role == 'tailor':
            return Project.objects.filter(user=user)
        
        # If the user is a customer, filter by their profile
        return Project.objects.filter(customer__user=user)

    def perform_create(self, serializer):
        # Assign the logged-in tailor as the project owner
        serializer.save(user=self.request.user)

# Detailed view of a single project
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Allow both the tailor AND the customer to retrieve the details
        if hasattr(user, 'profile') and user.profile.role == 'tailor':
            return Project.objects.filter(user=user)
        return Project.objects.filter(customer__user=user)

# View to post a progress update
class ProjectUpdateCreateView(generics.CreateAPIView):
    serializer_class = ProjectUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # You might want to add logic here to ensure only the 
        # assigned tailor can create an update
        serializer.save()