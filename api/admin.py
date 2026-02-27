from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# This ensures the 'role' field shows up in the Django Admin panel
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'phone_number')}),
    )

admin.site.register(User, CustomUserAdmin)