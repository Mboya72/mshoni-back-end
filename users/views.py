from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, RegisterSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Auto-generate tokens upon registration
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(email=request.data['email'])
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': response.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user.role 
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """
    This view handles the POST /api/users/login/ request 
    from your Flutter AuthService.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Ensure your custom User model uses email as the username field
        user = authenticate(username=email, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role,
                'first_name': user.first_name,
                'email': user.email
            }, status=status.HTTP_200_OK)
            
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # This receives the 'token' and 'role' from Flutter
        token = request.data.get('token')
        role = request.data.get('role', 'customer')
        
        # TODO: Implement google-auth verification logic
        return Response({'message': 'Google verification logic pending'}, status=status.HTTP_501_NOT_IMPLEMENTED)

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user