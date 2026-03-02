from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    TailorProfile, CustomerProfile, SellerProfile, JobPost, 
    Bid, Project, Measurement, ServiceMenu, LookbookItem, 
    Message, Tag, Notification
)

User = get_user_model()

# --- AUTH SERIALIZERS ---

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role', 'phone_number']

    def create(self, validated_data):
        # Extracts password to hash it properly via create_user
        user = User.objects.create_user(**validated_data)
        
        # Automatically create the profile based on the chosen role
        if user.role == 'TAILOR':
            TailorProfile.objects.create(user=user)
        elif user.role == 'CUSTOMER':
            CustomerProfile.objects.create(user=user)
        elif user.role == 'SELLER':
            # Note: We added SellerProfile in the model fix
            SellerProfile.objects.create(user=user, shop_name=f"{user.username}'s Shop")
            
        return user

class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'role_display', 'phone_number']

# --- PROFILE & SERVICE SERIALIZERS ---

class ServiceMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceMenu
        fields = ['id', 'name', 'price', 'estimated_days']

class LookbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookbookItem
        fields = ['id', 'image', 'description', 'style_category']

class TailorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    services = ServiceMenuSerializer(many=True, read_only=True)
    lookbook = LookbookSerializer(many=True, read_only=True)
    
    class Meta:
        model = TailorProfile
        fields = ['user', 'bio', 'location', 'rating', 'services', 'lookbook']

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['user', 'bio', 'location', 'preferences']

# --- JOB & BIDDING SERIALIZERS ---

class BidSerializer(serializers.ModelSerializer):
    tailor_name = serializers.ReadOnlyField(source='tailor.username')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'job', 'tailor', 'tailor_name', 'amount', 'proposal', 'status', 'status_display']
        read_only_fields = ['tailor']

class JobPostSerializer(serializers.ModelSerializer):
    bids = BidSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source='customer.username')
    bid_count = serializers.IntegerField(source='bids.count', read_only=True)

    class Meta:
        model = JobPost
        fields = ['id', 'customer', 'customer_name', 'title', 'description', 'is_open_for_bidding', 'budget', 'bids', 'bid_count', 'created_at']
        read_only_fields = ['customer']

# --- TRACKING & MESSAGING ---

class ProjectStatusSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'status', 'status_display', 'is_paid', 'due_date', 'total_cost']

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'label', 'data']

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source='sender.username')
    receiver_name = serializers.ReadOnlyField(source='receiver.username')
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'receiver', 'receiver_name', 'content', 'timestamp', 'is_read']
        read_only_fields = ['sender', 'timestamp']

# --- ADMIN & UTILITY ---

class TagSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.username')
    
    class Meta:
        model = Tag
        fields = ['id', 'tailor', 'customer', 'customer_name', 'label', 'notes', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'is_read']