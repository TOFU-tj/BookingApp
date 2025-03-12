from django.urls import reverse_lazy
from services.forms import ServiceModelForm, WorkScheduleForm 
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.list import ListView
from services.models import ServiceModel, WorkSchedule
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View



class WorkScheduleCreateView(CreateView):
    model = WorkSchedule
    form_class = WorkScheduleForm
    template_name = "services/work_schedule.html"  # Шаблон с календарем
    success_url = reverse_lazy("service:schedule_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_available = True  # Устанавливаем значение True для рабочего дня
        return super().form_valid(form)


class WorkScheduleListView(LoginRequiredMixin, ListView):
    model = WorkSchedule
    template_name = "services/schedule_list.html"
    context_object_name = "schedules"
    
    def get_queryset(self):
        return WorkSchedule.objects.filter(user=self.request.user) 







class WorkScheduleDelete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        schedule = get_object_or_404(WorkSchedule, pk=kwargs["pk"])

        schedule.delete()
        
        return redirect('service:schedule_list')


class ServiceView(LoginRequiredMixin, ListView):
    model = ServiceModel
    template_name = 'services/service_page.html'
    context_object_name = 'services'  
    
    def get_queryset(self):
        return ServiceModel.objects.filter(user=self.request.user)

class ServiceAddView(CreateView): 
    template_name = 'services/service_add.html'
    form_class = ServiceModelForm
    model = ServiceModel
    
    def form_valid(self, form):
        service = form.save(commit=False)
        service.user = self.request.user  
        service.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('service:service_list') 
    

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = ServiceModel
    success_url = reverse_lazy('service:service_list')

    def get_queryset(self):
        return ServiceModel.objects.filter(user=self.request.user)


class ServiceUpdateView(UpdateView):
    model = ServiceModel
    template_name = 'services/service_update.html'
    fields = ['name', 'description', 'price']
    success_url = reverse_lazy('service:service_list')

    def get_queryset(self):
        return ServiceModel.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = self.object
        return context