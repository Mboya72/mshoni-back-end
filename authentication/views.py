from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from users.models import User

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    # 1. Extract data from Flutter request
    email = request.data.get("email")
    password = request.data.get("password")
    first_name = request.data.get("first_name", "")
    role = request.data.get("role", "tailor")
    username = request.data.get("username")

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=400)

    # 2. Generate username if not provided
    if not username:
        username = email.split('@')[0] + get_random_string(5)

    # 3. Create User
    if User.objects.filter(email=email).exists():
        return Response({"error": "User with this email already exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        role=role
    )

    # 4. Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role
        }
    })

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Please provide both email and password"}, status=400)

    user = authenticate(request, username=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'first_name': user.first_name
            }
        })
    else:
        return Response({"error": "Invalid email or password"}, status=401)