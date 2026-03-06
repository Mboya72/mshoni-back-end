from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

# Google Auth imports
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Safely fetch user by email
        user = User.objects.get(email=request.data['email'])
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': response.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user.role 
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Ensure email is used for authentication
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
        token = request.data.get('token')
        assigned_role = request.data.get('role', 'customer')

        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the ID Token with Google
            # Ensure GOOGLE_CLIENT_ID is in your settings.py or .env
            client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
            
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                client_id
            )

            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')

            # Find or Create the User
            # We use email as the unique identifier
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email, # Most custom user models use email for username
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': assigned_role,
                }
            )

            refresh = RefreshToken.for_user(user)
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'role': user.role,
                'email': user.email,
                'first_name': user.first_name,
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': f'Invalid Google Token: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # This prevents the 500 error by returning a 400 with the error message
            return Response({'error': f'Backend Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user