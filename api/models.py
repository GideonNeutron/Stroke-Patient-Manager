from django.db import models
from django.contrib.auth.models import User

class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    key = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.key[:8]}...)"

class APIUsageLog(models.Model):
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE, related_name='usage_logs')
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10)  # GET, POST, etc.
    status_code = models.IntegerField()
    response_time = models.FloatField()  # in seconds
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()

    class Meta:
        ordering = ['-timestamp']

class APIRateLimit(models.Model):
    PERIOD_CHOICES = [
        ('SECOND', 'Per Second'),
        ('MINUTE', 'Per Minute'),
        ('HOUR', 'Per Hour'),
        ('DAY', 'Per Day')
    ]

    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE, related_name='rate_limits')
    endpoint = models.CharField(max_length=200, blank=True)  # blank means applies to all endpoints
    max_requests = models.IntegerField()
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('api_key', 'endpoint', 'period') 