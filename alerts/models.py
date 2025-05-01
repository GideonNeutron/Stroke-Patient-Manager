from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from patients.models import Patient
from neurologists.models import Neurologist

class Alert(models.Model):
    PRIORITY_CHOICES = [
        ('CRITICAL', 'Critical'),
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low')
    ]

    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('READ', 'Read'),
        ('ACKNOWLEDGED', 'Acknowledged'),
        ('RESOLVED', 'Resolved')
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='NEW')
    
    # Who created the alert
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_alerts')
    
    # Who should receive the alert
    recipients = models.ManyToManyField(User, related_name='received_alerts')
    
    # Generic foreign key to link to any model (Patient, VitalSigns, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_priority_display()} Alert: {self.title}"

class AlertRule(models.Model):
    """Rules for automatically generating alerts based on conditions"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    # Example: VitalSigns model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    
    # JSON field to store rule conditions
    conditions = models.JSONField()
    
    # Alert details
    alert_title_template = models.CharField(max_length=200)
    alert_message_template = models.TextField()
    alert_priority = models.CharField(max_length=10, choices=Alert.PRIORITY_CHOICES, default='MEDIUM')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AlertLog(models.Model):
    """Log of alert notifications sent"""
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='notification_logs')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=50)  # e.g., 'sent', 'failed', 'delivered'
    notification_method = models.CharField(max_length=50)  # e.g., 'email', 'sms', 'in-app'

    class Meta:
        ordering = ['-sent_at'] 