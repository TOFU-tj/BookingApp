from django.urls import reverse
from django.views.generic import ListView, CreateView
from services.models import ServiceModel, WorkSchedule
from client_web.models import Basket, UserForm
from client_web.forms import UserBlank
from django.shortcuts import render, redirect, get_object_or_404






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



class BasketTemplateView(ListView):
    model = Basket
    template_name = 'client_web/basket.html'
    context_object_name = 'basket'

    def get_queryset(self):
        return Basket.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug_company'] = self.kwargs.get('slug_company', '')  # Получаем из URL
        context['slug_username'] = self.kwargs.get('slug_username', '')  # Получаем из URL
        return context

    
    
    
from django.urls import reverse_lazy

class UserFormView(CreateView): 
    model = UserForm
    form_class = UserBlank
    template_name = 'client_web/user_form.html'
    
    success_url = reverse_lazy('client:client_basket')



def add_to_basket(request, slug_company, slug_username, item_id):
    service = get_object_or_404(ServiceModel, id=item_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # Проверяем, есть ли уже этот сервис в корзине для текущего пользователя
    basket_item = Basket.objects.filter(session_key=session_key, service=service).first()

    if not basket_item:
        # Если сервис не найден в корзине, создаем новый элемент с указанными параметрами
        Basket.objects.create(session_key=session_key, service=service, quantity=1)
    else:
        # Если сервис уже есть в корзине, увеличиваем его количество
        basket_item.quantity = 1
        basket_item.save()

    return redirect(request.META.get("HTTP_REFERER", "/"))


