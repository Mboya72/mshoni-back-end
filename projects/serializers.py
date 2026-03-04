from rest_framework import serializers
from .models import Project, ProjectUpdate

class ProjectUpdateSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ProjectUpdate
        fields = ['id', 'project', 'status', 'status_display', 'description', 'image', 'timestamp']

class ProjectSerializer(serializers.ModelSerializer):
    updates = ProjectUpdateSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source='customer.user.username')

    class Meta:
        model = Project
        fields = '__all__'