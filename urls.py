from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    dashboard, patients_list, patient_detail,
    neurologists_list, neurologist_detail,
    consultations_list, consultation_detail,
    alerts_list, alert_detail
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('patients/', patients_list, name='patients_list'),
    path('patients/<int:pk>/', patient_detail, name='patient_detail'),
    path('neurologists/', neurologists_list, name='neurologists_list'),
    path('neurologists/<int:pk>/', neurologist_detail, name='neurologist_detail'),
    path('consultations/', consultations_list, name='consultations_list'),
    path('consultations/<int:pk>/', consultation_detail, name='consultation_detail'),
    path('alerts/', alerts_list, name='alerts_list'),
    path('alerts/<int:pk>/', alert_detail, name='alert_detail'),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add debug toolbar URLs in development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns 