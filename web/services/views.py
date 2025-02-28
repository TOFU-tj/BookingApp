from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from services.forms import ServiceModelForm, WorkScheduleForm, AppointmentForm
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from services.models import ServiceModel, WorkSchedule, Appointment


from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


from django.http import JsonResponse



class WorkScheduleCreateView(LoginRequiredMixin, CreateView):
    model = WorkSchedule
    form_class = WorkScheduleForm
    template_name = "services/work_schedule.html"  
    success_url = reverse_lazy("service:schedule_list")

    def form_valid(self, form):
        form.instance.user = self.request.user  # Привязываем к авторизованному пользователю
        return super().form_valid(form)




class WorkScheduleListView(LoginRequiredMixin, ListView):
    model = WorkSchedule
    template_name = "services/schedule_list.html"
    context_object_name = "schedules"

    def get_queryset(self):
        return WorkSchedule.objects.filter(user=self.request.user) 




from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import WorkSchedule

class WorkScheduleDelete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        schedule = get_object_or_404(WorkSchedule, pk=kwargs["pk"])

        schedule.delete()
        
        return redirect('service:schedule_list')



# class AppointmentCreateView(CreateView):
#     model = Appointment
#     form_class = AppointmentForm
#     template_name = "services/appointment_form.html"  
#     success_url = reverse_lazy("service:schedule_list")
    

#     def form_valid(self, form):
#         master = form.cleaned_data['master']
#         date = form.cleaned_data['date']
#         time = form.cleaned_data['time']

#         # Проверяем, занято ли уже это время
#         if Appointment.objects.filter(master=master, date=date, time=time).exists():
#             return JsonResponse({"success": False, "error": "Это время уже занято!"}, status=400)

#         return super().form_valid(form)





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