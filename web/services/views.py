from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from services.forms import ServiceModelForm, ScheduleModelForm
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from services.models import ServiceModel, ScheduleModel
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin



class ScheduleListView(ListView):
    template_name = "services/schedule_admin.html"
    model = ScheduleModel
    context_object_name = "schedules"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ScheduleModelForm()  # Форма для добавления
        return context
 


class ScheduleCreateView(CreateView):
    model = ScheduleModel
    form_class = ScheduleModelForm
    template_name = "services/schedule_add.html"  
    success_url = reverse_lazy("service:schedule")

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


    


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