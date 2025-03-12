from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from client_web.models import Basket, SuccessModel, UserForm, User


class MainViews(LoginRequiredMixin, ListView):
    model = SuccessModel
    template_name = 'main_page/main.html'
    context_object_name = "records"

    def get_queryset(self):
        return SuccessModel.objects.filter(executor=self.request.user)  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        last_record = self.get_queryset().last()  # Берем последнюю запись
        
        if last_record:
            context["user"] = last_record.name  # Данные клиента
            context["basket_items"] = Basket.objects.filter(session_key=last_record.basket.session_key)  # Все услуги из корзины
        
        return context

    
    
from django.shortcuts import get_object_or_404

def create_appointment(request, slug_company, slug_username):
    """Создает запись клиента к конкретному владельцу компании"""
    if request.method == "POST":
        # Получаем владельца компании (исполнителя)
        executor = get_object_or_404(User, slug_company=slug_company, slug_username=slug_username)

        # Создаем форму клиента
        user_form = UserForm.objects.create(
            name=request.POST["name"],
            surname=request.POST["surname"],
            phone=request.POST["phone"],
            email=request.POST["email"]
        )

        # Создаем корзину с услугами (если у тебя она как-то иначе заполняется — исправь тут)
        basket = Basket.objects.create(
            service_id=request.POST["service_id"],
            quantity=request.POST["quantity"]
        )

        # Создаем запись
        SuccessModel.objects.create(
            name=user_form,
            basket=basket,
            executor=executor  # Владелец компании
        )

        return redirect("main:main")  # Перенаправляем на главную страницу
    return redirect("main:main")  # Если не POST-запрос, просто редиректим


def generate_client_service_link(request):
    user = request.user

    # Ensure only the necessary fields are being used for URL reversal
    if user.is_authenticated and user.slug_company and user.slug_username:
        # Generate the link with the correct parameters only
        link = request.build_absolute_uri(reverse(
            'client:client_services', 
            kwargs={'slug_company': user.slug_company, 'slug_username': user.slug_username}
        ))
        return render(request, 'main_page/link.html', {'link': link})
    else:
        # If the necessary data is missing, return an error
        return render(request, 'main_page/link.html', {'error': 'Не удалось создать ссылку.'})
