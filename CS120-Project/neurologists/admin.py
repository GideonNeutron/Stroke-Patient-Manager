from django.contrib import admin
from .models import Neurologist, Consultation, TreatmentOrder, TestOrder

@admin.register(Neurologist)
class NeurologistAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'hospital_affiliation', 'is_available')
    list_filter = ('is_available', 'hospital_affiliation')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'license_number')

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'neurologist', 'status', 'created_at', 'completed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('patient__name', 'neurologist__user__username', 'diagnosis')
    date_hierarchy = 'created_at'

@admin.register(TreatmentOrder)
class TreatmentOrderAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'treatment_type', 'priority', 'is_completed', 'created_at')
    list_filter = ('priority', 'is_completed', 'created_at')
    search_fields = ('consultation__patient__name', 'treatment_type', 'instructions')
    date_hierarchy = 'created_at'

@admin.register(TestOrder)
class TestOrderAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'test_name', 'is_completed', 'created_at')
    list_filter = ('is_completed', 'created_at')
    search_fields = ('consultation__patient__name', 'test_name', 'instructions')
    date_hierarchy = 'created_at' 