from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    # Pulls the actual Cloudinary URL from the related MediaFile
    profile_picture_url = serializers.SerializerMethodField()
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'role_display', 'profile_picture', 'profile_picture_url'
        )
        read_only_fields = ('email',)

    def get_profile_picture_url(self, obj):
        if obj.profile_picture and hasattr(obj.profile_picture, 'file'):
            return obj.profile_picture.file.url
        return None

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'first_name': {'required': True},
            'username': {'required': False} # Allow manager to generate if blank
        }

    def create(self, validated_data):
        # This calls our custom UserManager.create_user logic
        return User.objects.create_user(**validated_data)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims into the Encrypted Token (useful for frontend decoding)
        token['role'] = user.role
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add extra data to the raw JSON response for immediate use in Flutter
        data['role'] = self.user.role
        data['username'] = self.user.username
        data['user_id'] = self.user.id
        # Include profile picture URL in the login response
        if self.user.profile_picture:
            data['profile_picture'] = self.user.profile_picture.file.url
        else:
            data['profile_picture'] = None
            
        return data