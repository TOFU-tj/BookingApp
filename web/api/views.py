from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from services.models import ServiceModel
from services.serializers import ServiceModelSerializer
from rest_framework.permissions import IsAdminUser
# from rest_framework.permissions import IsAuthenticatedOrReadOnly



class ServiceListAPIView(ModelViewSet):
    queryset = ServiceModel.objects.all()
    serializer_class = ServiceModelSerializer
    permission_classes = [IsAdminUser]  

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'): 
            self.permission_classes = [IsAdminUser]  # Должно быть списком
        return super().get_permissions()
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
    
    