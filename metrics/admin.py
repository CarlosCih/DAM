from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category', 'assigned_to', 'created_at', 'updated_at')
    search_fields = ('title', 'assigned_to')
    list_filter = ('status', 'category', 'created_at', 'updated_at')
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ticket, TicketAdmin)
