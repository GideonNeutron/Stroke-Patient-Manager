from django.contrib import admin
from .models import Alert, AlertRule, AlertLog

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'created_by', 'created_at')
    list_filter = ('priority', 'status', 'created_at')
    search_fields = ('title', 'message', 'created_by__username')
    date_hierarchy = 'created_at'
    filter_horizontal = ('recipients',)

@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'alert_priority', 'is_active')
    list_filter = ('is_active', 'alert_priority', 'content_type')
    search_fields = ('name', 'description')

@admin.register(AlertLog)
class AlertLogAdmin(admin.ModelAdmin):
    list_display = ('alert', 'recipient', 'sent_at', 'delivery_status', 'notification_method')
    list_filter = ('delivery_status', 'notification_method', 'sent_at')
    search_fields = ('alert__title', 'recipient__username')
    date_hierarchy = 'sent_at' 