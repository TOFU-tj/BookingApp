from rest_framework import serializers
from services.models import ServiceModel, WorkSchedule
from user.serializers import UserModelSerializer

from user.models import User


class ServiceModelSerializer(serializers.ModelSerializer): 
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(), 
        slug_field="username"  
    )

    class Meta: 
        model = ServiceModel
        fields = '__all__'


class WorkScheduleSerializer(serializers.ModelSerializer): 
    class Meta : 
        model = WorkSchedule
        fields = "__all__"