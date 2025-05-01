from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)])
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    chief_complaint = models.TextField()
    medical_history = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.age})"

class VitalSigns(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_signs')
    blood_pressure_systolic = models.IntegerField()
    blood_pressure_diastolic = models.IntegerField()
    heart_rate = models.IntegerField()
    respiratory_rate = models.IntegerField()
    oxygen_saturation = models.DecimalField(max_digits=4, decimal_places=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class LabResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=100)
    result_value = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    reference_range = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class Imaging(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='imaging_studies')
    study_type = models.CharField(max_length=100)  # e.g., CT, MRI
    findings = models.TextField()
    image_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Imaging Studies'

class NIHSSScore(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='nihss_scores')
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(42)])
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'NIHSS Score'
        verbose_name_plural = 'NIHSS Scores' 