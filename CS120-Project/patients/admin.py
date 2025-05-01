from django.contrib import admin
from .models import Patient, VitalSigns, LabResult, Imaging, NIHSSScore

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'sex', 'created_at')
    list_filter = ('sex', 'created_at')
    search_fields = ('name', 'medical_history')
    date_hierarchy = 'created_at'

@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'blood_pressure_systolic', 'blood_pressure_diastolic', 
                   'heart_rate', 'oxygen_saturation', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('patient__name',)
    date_hierarchy = 'timestamp'

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test_name', 'result_value', 'unit', 'timestamp')
    list_filter = ('test_name', 'timestamp')
    search_fields = ('patient__name', 'test_name')
    date_hierarchy = 'timestamp'

@admin.register(Imaging)
class ImagingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'study_type', 'timestamp')
    list_filter = ('study_type', 'timestamp')
    search_fields = ('patient__name', 'findings')
    date_hierarchy = 'timestamp'

@admin.register(NIHSSScore)
class NIHSSScoreAdmin(admin.ModelAdmin):
    list_display = ('patient', 'score', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('patient__name', 'notes')
 