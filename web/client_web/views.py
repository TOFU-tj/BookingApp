from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from services.models import ServiceModel, WorkSchedule
from client_web.models import Basket

class ClientServicesListView(ListView): 
    model = ServiceModel
    template_name = 'client_web/client_page.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return ServiceModel.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug_company'] = self.kwargs.get('slug_company', '')
        context['slug_username'] = self.kwargs.get('slug_username', '')
        return context

    
       
class WorkScheduleListView(ListView): 
    model = WorkSchedule
    template_name= 'templates/schedule_page.html'
    context_object_name = 'schedule'
    
    def get_queryset(self):
        return WorkSchedule.objects.filter(user=self.request.user)
    


def basket_page(request): 
    """Вывод страницы корзины"""
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        basket = Basket.objects.filter(session_key=request.session.session_key)
    
    context = {'basket': basket}
    return render(request, 'client_basket/basket.html', context)

