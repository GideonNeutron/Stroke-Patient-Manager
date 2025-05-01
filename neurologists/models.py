from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient

class Neurologist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)
    hospital_affiliation = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class Consultation(models.Model):
    STATUS_CHOICES = [
        ('REQUESTED', 'Consultation Requested'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    neurologist = models.ForeignKey(Neurologist, on_delete=models.CASCADE, related_name='consultations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    diagnosis = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

class TreatmentOrder(models.Model):
    PRIORITY_CHOICES = [
        ('HIGH', 'High Priority'),
        ('MEDIUM', 'Medium Priority'),
        ('LOW', 'Low Priority')
    ]

    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='treatment_orders')
    treatment_type = models.CharField(max_length=100)
    instructions = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

class TestOrder(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='test_orders')
    test_name = models.CharField(max_length=100)
    instructions = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    results = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at'] 