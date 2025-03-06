from rest_framework.viewsets import ModelViewSet
from services.models import ServiceModel, WorkSchedule
from user.models import User
from services.serializers import ServiceModelSerializer, WorkScheduleSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

# Ваша функция ServiceListAPIView должна учитывать правильное регулярное выражение
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from services.models import ServiceModel

class ServiceListAPIView(ModelViewSet):
    serializer_class = ServiceModelSerializer

    def get_queryset(self):
        username = self.kwargs['username']  # Получаем username из URL
        company_slug = self.kwargs['company_slug']  # Получаем company_slug из URL
        # Вставляем логику фильтрации
        user = get_object_or_404(User, slug_username=username, slug_company=company_slug)
        return ServiceModel.objects.filter(user=user)

    def perform_create(self, serializer):
        username = self.kwargs['username']
        company_slug = self.kwargs['company_slug']
        user = get_object_or_404(User, slug_username=username, slug_company=company_slug)
        serializer.save(user=user)


class WorkScheduleApiView(ModelViewSet):
    serializer_class = WorkScheduleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        username = self.kwargs.get('username')  # Извлекаем параметры из URL
        company_slug = self.kwargs.get('company_slug')

        user = get_object_or_404(User, slug_username=username, slug_company=company_slug)

        return WorkSchedule.objects.filter(user=user)

    def perform_create(self, serializer):
        username = self.kwargs.get('username')
        company_slug = self.kwargs.get('company_slug')

        user = get_object_or_404(User, slug_username=username, slug_company=company_slug)
        serializer.save(user=user)
