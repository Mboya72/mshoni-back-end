from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Add your custom fields to the list view
    list_display = ('email', 'username', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    
    # Add your custom fields to the edit forms
    fieldsets = UserAdmin.fieldsets + (
        ('Mshoni Profile', {'fields': ('role', 'profile_picture')}),
    )
    
    # Add your custom fields to the "Add User" form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Mshoni Profile', {'fields': ('role', 'profile_picture')}),
    )

admin.site.register(User, CustomUserAdmin)