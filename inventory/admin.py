from django.contrib import admin
from .models import Inventory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'quantity', 'unit_type', 'is_featured', 'is_available')
    list_filter = ('category', 'is_featured', 'is_available')
    search_fields = ('name', 'user__username')
    list_editable = ('is_featured', 'is_available')