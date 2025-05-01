"""
URL configuration for stroke_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import (
    dashboard, patients_list, patient_detail,
    neurologists_list, neurologist_detail,
    consultations_list, consultation_detail,
    alerts_list, alert_detail, register, profile
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', next_page='profile'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    
    # Application URLs
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
