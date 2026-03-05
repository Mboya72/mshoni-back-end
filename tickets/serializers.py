from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    # We display the email or username of the creator and assignee for the Flutter UI
    creator_email = serializers.ReadOnlyField(source='creator.email')
    assigned_to_name = serializers.ReadOnlyField(source='assigned_to.username')
    
    # We can also pull in the membership tier to help Support prioritize
    membership_tier = serializers.ReadOnlyField(source='creator.profile.membership_tier')

    class Meta:
        model = Ticket
        fields = [
            'id', 'category', 'subject', 'description', 
            'project', 'status', 'priority', 'creator_email', 
            'assigned_to_name', 'membership_tier', 'date_created', 'date_updated'
        ]
        # We make these read-only so a user can't manually set 
        # themselves as 'Resolved' or change the creator ID via Postman/Flutter.
        read_only_fields = ('id', 'creator', 'status', 'date_created', 'date_updated', 'assigned_to')

    def validate_project(self, value):
        """
        Custom validation: Ensure the ticket creator actually 
        owns or is part of the project they are complaining about.
        """
        user = self.context['request'].user
        if value and user not in [value.customer, value.tailor]:
            raise serializers.ValidationError("You can only open disputes for your own projects.")
        return value