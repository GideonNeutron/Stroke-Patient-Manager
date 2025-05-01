from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import APIKey, APIUsageLog

# Add signal handlers here when needed 