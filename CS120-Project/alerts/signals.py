from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Alert, AlertRule

# Add signal handlers here when needed 