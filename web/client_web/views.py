
from django.views.generic import ListView
from services.models import ServiceModel, WorkSchedule
from client_web.models import Basket
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

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
    template_name = 'client_web/schedule_page.html'
    context_object_name = 'work_schedule'
    
    def get_queryset(self):
        # Возвращаем все рабочие расписания (без фильтрации по услуге)
        return WorkSchedule.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # В контекст передаем все рабочие расписания
        context['slug_company'] = self.kwargs.get('slug_company', '')
        context['slug_username'] = self.kwargs.get('slug_username', '')
        
        return context

    

class BasketTemplateView(ListView):
    model = Basket
    context_object_name = 'basket'
    template_name = 'client_web/basket.html'
    
    def get_queryset(self):
        # Получаем session_key (для анонимных пользователей)
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.create()
            session_key = self.request.session.session_key

        return Basket.objects.filter(session_key=session_key)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем slug_company и slug_username в контекст, если они есть
        context['slug_company'] = self.kwargs.get('slug_company', '')
        context['slug_username'] = self.kwargs.get('slug_username', '')
        return context

    


def remove_from_basket(request, item_id, slug_company, slug_username):
    if request.method == "POST":
        # Находим товар в корзине по ID
        basket_item = get_object_or_404(Basket, id=item_id)

        # Удаляем товар
        basket_item.delete()

        # Перенаправляем обратно на страницу корзины с переданными параметрами
        return redirect('client:basket_list', slug_company=slug_company, slug_username=slug_username)

    # Если не POST, перенаправляем на страницу корзины по умолчанию с переданными параметрами
    return redirect('client:basket_list', slug_company=slug_company, slug_username=slug_username)





def add_to_basket(request, slug_company, slug_username):
    try:
        if request.method == "POST":
            service_id = request.POST.get("service_id")

            if not service_id:
                return JsonResponse({"success": False, "message": "ID услуги не передан."})

            # Получаем услугу по ID
            service = get_object_or_404(ServiceModel, id=service_id)

            # Получаем session_key, если его нет — создаем новый
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            # Добавляем товар в корзину по session_key
            basket_item, created = Basket.objects.get_or_create(
                session_key=session_key,
                service=service,
            )

            if not created:
                basket_item.quantity = 1  # Если товар уже есть в корзине, увеличиваем количество
                basket_item.save()

            # Возвращаем успешный ответ в формате JSON
            return JsonResponse({"success": True, "message": "Товар добавлен в корзину!"})
        
        # Если метод не POST, перенаправляем обратно на страницу услуг
        return redirect('client:client_services', slug_company=slug_company, slug_username=slug_username)

    except Exception as e:
        # Логирование ошибки и отправка сообщения об ошибке
        print(f"Ошибка при добавлении в корзину: {e}")
        return JsonResponse({"success": False, "message": "Произошла ошибка при добавлении в корзину."})
