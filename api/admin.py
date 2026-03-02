from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, TailorProfile, CustomerProfile, SellerProfile,
    ServiceMenu, LookbookItem, JobPost, Bid, Project,
    Material, Appointment, Measurement, Message, Tag, Notification
)

# --- INLINES ---
# These allow you to edit related data on the same page (e.g., edit services inside the Tailor page)

class ServiceMenuInline(admin.TabularInline):
    model = ServiceMenu
    extra = 1

class LookbookInline(admin.StackedInline):
    model = LookbookItem
    extra = 1

# --- CUSTOM USER ADMIN ---

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone_number', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'phone_number', 'whatsapp_enabled')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('role', 'phone_number', 'whatsapp_enabled')}),
    )

# --- PROFILE ADMINS ---

@admin.register(TailorProfile)
class TailorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'rating')
    search_fields = ('user__username', 'location')
    inlines = [ServiceMenuInline, LookbookInline]

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location')
    search_fields = ('user__username',)

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user')
    search_fields = ('shop_name', 'user__username')

# --- BUSINESS LOGIC ADMINS ---

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'budget', 'is_open_for_bidding', 'created_at')
    list_filter = ('is_open_for_bidding', 'created_at')
    search_fields = ('title', 'customer__username')

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('job', 'tailor', 'amount', 'status')
    list_filter = ('status',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'tailor', 'customer', 'status', 'due_date', 'is_paid')
    list_filter = ('status', 'is_paid')
    search_fields = ('tailor__username', 'customer__username')
    date_hierarchy = 'due_date'

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'stock_quantity')
    list_filter = ('category',)
    search_fields = ('name', 'seller__shop_name')

# --- UTILITY ADMINS ---

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'is_read')
    date_hierarchy = 'timestamp'

admin.site.register(Measurement)
admin.site.register(Appointment)
admin.site.register(Notification)
admin.site.register(Tag)