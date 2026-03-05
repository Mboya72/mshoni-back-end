from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    # This nests the basic user info inside the profile
    user = UserSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'role', 'role_display', 'bio', 
            'profile_picture', 'phone_number', 'location', 
            'is_verified', 'rating'
        ]