from django.urls import reverse
from django.views.generic import ListView, CreateView
from services.models import ServiceModel, WorkSchedule
from client_web.models import Basket, UserForm, SuccessModel, User
from client_web.forms import UserBlank
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View





class ClientServicesListView(ListView):
    model = ServiceModel
    template_name = 'client_web/client_page.html'
    context_object_name = 'services'

    def get_queryset(self):
        slug_username = self.kwargs.get('slug_username')  # Получаем исполнителя из URL
        return ServiceModel.objects.filter(user__username=slug_username)  # Фильтруем услуги по этому пользователю

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug_company'] = self.kwargs.get('slug_company', '')
        context['slug_username'] = self.kwargs.get('slug_username', '')

        # Передаём в шаблон текущего исполнителя
        context['executor'] = get_object_or_404(User, username=self.kwargs['slug_username'])
        return context




class BasketTemplateView(ListView):
    model = Basket
    template_name = 'client_web/basket.html'
    context_object_name = 'basket'

    def get_queryset(self):
        slug_username = self.kwargs.get('slug_username')  # Определяем исполнителя
        return Basket.objects.filter(service__user__username=slug_username)  # Фильтруем корзину

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug_company'] = self.kwargs.get('slug_company', '')  
        context['slug_username'] = self.kwargs.get('slug_username', '')  

        # Передаём текущего исполнителя
        context['executor'] = get_object_or_404(User, username=self.kwargs['slug_username'])
        return context



def add_to_basket(request, slug_company, slug_username, item_id):
    service = get_object_or_404(ServiceModel, id=item_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    executor = get_object_or_404(User, username=slug_username)

    # Проверяем, есть ли уже эта услуга в корзине
    basket_item, created = Basket.objects.get_or_create(
        session_key=session_key,
        service=service,
        executor=executor,  # Привязываем корзину к конкретному специалисту
        defaults={'quantity': 1}
    )

    if not created:
        basket_item.quantity += 1
        basket_item.save()

    return redirect(request.META.get("HTTP_REFERER", "/"))

    
    


class BasketDeleteView(View):
    def post(self, request, slug_company, slug_username, item_id):
        session_key = request.session.session_key
        if session_key:
            Basket.objects.filter(session_key=session_key, id=item_id).delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))

    
    
    
    
from django.urls import reverse_lazy

class UserFormView(CreateView): 
    model = UserForm
    form_class = UserBlank
    template_name = 'client_web/user_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 🔥 Определяем текущего исполнителя (executor) по slug_username
        executor = get_object_or_404(User, username=self.kwargs["slug_username"])

        # ✅ Фильтруем только расписания этого исполнителя
        context["schedules"] = WorkSchedule.objects.filter(is_available=True, user=executor)

        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.create()
            session_key = self.request.session.session_key

        basket = Basket.objects.filter(session_key=session_key).first()
        if not basket:
            return redirect("client:client_basket", slug_company=self.kwargs["slug_company"], slug_username=self.kwargs["slug_username"])

        form.instance.basket = basket
        user_form = form.save()

        # 🔥 Автоматически определяем исполнителя (executor) по slug_username
        executor = get_object_or_404(User, username=self.kwargs["slug_username"])

        # ✅ Создаем запись в SuccessModel с заполненным executor
        SuccessModel.objects.create(name=user_form, basket=basket, executor=executor)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'client:success', 
            kwargs={
                "slug_company": self.kwargs["slug_company"],
                "slug_username": self.kwargs["slug_username"],
            }
        )






class SuccessView(ListView): 
    model = SuccessModel
    template_name = 'client_web/success.html'
    context_object_name = 'success_entries'

    def get_queryset(self):
        session_key = self.request.session.session_key
        if not session_key:
            return SuccessModel.objects.none()
        return SuccessModel.objects.filter(basket__session_key=session_key).select_related('name', 'basket')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_entry = self.get_queryset().last()
        
        if last_entry:
            context["user"] = last_entry.name  
            context["basket_items"] = Basket.objects.filter(session_key=self.request.session.session_key)

        return context