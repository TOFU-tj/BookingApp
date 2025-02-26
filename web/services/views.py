from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from services.forms import ServiceModelForm
from django.views.generic.edit import DeleteView
from services.models import ServiceModel
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin



class ServiceView(LoginRequiredMixin,TemplateView): 
    template_name = 'services/service_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = ServiceModel.objects.filter(user=self.request.user)
        return context


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

from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import ServiceModel



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