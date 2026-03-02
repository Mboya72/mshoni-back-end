from django.db.models import Q
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import (
    Measurement, LookbookItem, Message, Tag, 
    Notification, CustomerProfile, JobPost, Project
)
from .serializers import (
    RegisterSerializer, MeasurementSerializer, LookbookSerializer, 
    MessageSerializer, TagSerializer, NotificationSerializer, 
    CustomerProfileSerializer, JobPostSerializer, ProjectStatusSerializer
)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Account created successfully!",
                "token": token.key,
                "role": user.role,
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Measurement.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LookbookViewSet(viewsets.ModelViewSet):
    serializer_class = LookbookSerializer
    queryset = LookbookItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Prevent crash if a Customer tries to post a lookbook item
        if hasattr(self.request.user, 'tailor_profile'):
            serializer.save(tailor=self.request.user.tailor_profile)
        else:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Only tailors can maintain a lookbook.")

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'tailor_profile'):
            return Tag.objects.filter(tailor=self.request.user.tailor_profile)
        return Tag.objects.none()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'tailor_profile'):
            serializer.save(tailor=self.request.user.tailor_profile)

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CUSTOMER':
            return JobPost.objects.filter(customer=user)
        # Tailors see all open jobs to bid on them
        elif user.role == 'TAILOR':
            return JobPost.objects.filter(is_open_for_bidding=True)
        return JobPost.objects.all()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CUSTOMER':
            return Project.objects.filter(customer=user)
        elif user.role == 'TAILOR':
            return Project.objects.filter(tailor=user)
        return Project.objects.none()

    def perform_create(self, serializer):
        # Automatically assign the tailor who is creating the project tracking
        serializer.save(tailor=self.request.user)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')