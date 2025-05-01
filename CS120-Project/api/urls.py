from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, NeurologistViewSet, ConsultationViewSet,
    AlertViewSet, APIKeyViewSet
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'neurologists', NeurologistViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'alerts', AlertViewSet)
router.register(r'api-keys', APIKeyViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 