from django.contrib import admin
from .models import APIKey, APIUsageLog, APIRateLimit

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'key', 'is_active', 'created_at', 'expires_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'user__username', 'key')
    date_hierarchy = 'created_at'
    readonly_fields = ('key',)

@admin.register(APIUsageLog)
class APIUsageLogAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'endpoint', 'method', 'status_code', 'response_time', 'timestamp')
    list_filter = ('method', 'status_code', 'timestamp')
    search_fields = ('api_key__name', 'endpoint', 'ip_address')
    date_hierarchy = 'timestamp'

@admin.register(APIRateLimit)
class APIRateLimitAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'endpoint', 'max_requests', 'period')
    list_filter = ('period',)
    search_fields = ('api_key__name', 'endpoint') 