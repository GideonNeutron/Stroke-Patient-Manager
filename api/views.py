from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from patients.models import Patient, VitalSigns, LabResult, Imaging, NIHSSScore
from neurologists.models import Neurologist, Consultation, TreatmentOrder, TestOrder
from alerts.models import Alert, AlertRule, AlertLog
from .models import APIKey, APIUsageLog, APIRateLimit
from .serializers import (
    PatientSerializer, VitalSignsSerializer, LabResultSerializer,
    ImagingSerializer, NIHSSScoreSerializer, NeurologistSerializer,
    ConsultationSerializer, TreatmentOrderSerializer, TestOrderSerializer,
    AlertSerializer, AlertRuleSerializer, AlertLogSerializer,
    APIKeySerializer, APIUsageLogSerializer, APIRateLimitSerializer
)
from django.utils import timezone

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def vital_signs(self, request, pk=None):
        patient = self.get_object()
        vital_signs = VitalSigns.objects.filter(patient=patient)
        serializer = VitalSignsSerializer(vital_signs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def lab_results(self, request, pk=None):
        patient = self.get_object()
        lab_results = LabResult.objects.filter(patient=patient)
        serializer = LabResultSerializer(lab_results, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def imaging_studies(self, request, pk=None):
        patient = self.get_object()
        imaging = Imaging.objects.filter(patient=patient)
        serializer = ImagingSerializer(imaging, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def nihss_scores(self, request, pk=None):
        patient = self.get_object()
        scores = NIHSSScore.objects.filter(patient=patient)
        serializer = NIHSSScoreSerializer(scores, many=True)
        return Response(serializer.data)

class NeurologistViewSet(viewsets.ModelViewSet):
    queryset = Neurologist.objects.all()
    serializer_class = NeurologistSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def consultations(self, request, pk=None):
        neurologist = self.get_object()
        consultations = Consultation.objects.filter(neurologist=neurologist)
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        neurologist = self.get_object()
        neurologist.is_available = not neurologist.is_available
        neurologist.save()
        return Response({'status': 'availability updated'})

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        consultation = self.get_object()
        if consultation.status == 'IN_PROGRESS':
            consultation.status = 'COMPLETED'
            consultation.completed_at = timezone.now()
            consultation.save()
            return Response({'status': 'consultation completed'})
        return Response(
            {'error': 'Consultation must be in progress to complete'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def add_treatment_order(self, request, pk=None):
        consultation = self.get_object()
        serializer = TreatmentOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(consultation=consultation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_test_order(self, request, pk=None):
        consultation = self.get_object()
        serializer = TestOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(consultation=consultation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        alert = self.get_object()
        if alert.status == 'NEW' or alert.status == 'READ':
            alert.status = 'ACKNOWLEDGED'
            alert.acknowledged_at = timezone.now()
            alert.save()
            return Response({'status': 'alert acknowledged'})
        return Response(
            {'error': 'Alert must be new or read to acknowledge'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        if alert.status != 'RESOLVED':
            alert.status = 'RESOLVED'
            alert.resolved_at = timezone.now()
            alert.save()
            return Response({'status': 'alert resolved'})
        return Response(
            {'error': 'Alert is already resolved'},
            status=status.HTTP_400_BAD_REQUEST
        )

class APIKeyViewSet(viewsets.ModelViewSet):
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        api_key = self.get_object()
        api_key.is_active = False
        api_key.save()
        return Response({'status': 'api key deactivated'})

    @action(detail=True, methods=['get'])
    def usage_logs(self, request, pk=None):
        api_key = self.get_object()
        logs = APIUsageLog.objects.filter(api_key=api_key)
        serializer = APIUsageLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def rate_limits(self, request, pk=None):
        api_key = self.get_object()
        limits = APIRateLimit.objects.filter(api_key=api_key)
        serializer = APIRateLimitSerializer(limits, many=True)
        return Response(serializer.data)

# Create your views here. 