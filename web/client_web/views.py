from django.shortcuts import render
from django.views.generic import ListView
from services.models import ServiceModel, WorkSchedule


class ClientServicesListView(ListView): 
    model = ServiceModel
    template_name = 'client_web/client_page.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return ServiceModel.objects.filter(user=self.request.user)
    
    
       
class WorkScheduleListView(ListView): 
    model = WorkSchedule
    template_name= 'templates/schedule_page.html'
    context_object_name = 'schedule'
    
    def get_queryset(self):
        return WorkSchedule.objects.filter(user=self.request.user)
    