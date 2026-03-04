# media_file/views.py
from rest_framework import generics, permissions, parsers
from .models import MediaFile
from .serializers import MediaFileSerializer

class MediaUploadView(generics.CreateAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def perform_create(self, serializer):
        # This will automatically set the user when they upload
        serializer.save(uploaded_by=self.request.user)