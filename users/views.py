from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
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
            # 1. Fetch Client IDs
            # If you have separate IDs for Android/iOS, you can pass them as a list
            web_client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
            
            # 2. Verify Token
            # Passing the web_client_id as the audience
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                web_client_id
            )

            # 3. Validation Logic
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')

            # 4. Find or Create User
            # We use email for username to avoid split('@') collisions
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email, 
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': assigned_role,
                }
            )

            # 5. Token Generation
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'role': user.role,
                'email': user.email,
                'first_name': user.first_name,
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            # This will show up in your Render logs to tell you EXACTLY why it failed
            print(f"DEBUG: Google Validation Failed: {str(e)}")
            return Response({'error': f'Invalid Google Token: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"DEBUG: Unexpected Backend Error: {str(e)}")
            return Response({'error': f'Backend Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user