from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView
from services.models import ServiceModel
from client_web.models import Basket, UserForm, SuccessModel, User, ClientSchedule
from client_web.forms import UserBlank, ClientScheduleForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils import timezone
from datetime import timedelta
from schedule.models import  DaySchedule, TimeSlot
from django.http import JsonResponse
from django.contrib import messages


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
        session_key = self.request.session.session_key  # Получаем session_key текущего пользователя

        if not session_key:
            return Basket.objects.none()  # Если session_key отсутствует, возвращаем пустой QuerySet

        # Фильтруем корзину по исполнителю и session_key
        return Basket.objects.filter(
            service__user__username=slug_username,
            session_key=session_key
        ).select_related('service', 'executor')  # Оптимизация запросов

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
        request.session.create()  # Создаём новую сессию, если её нет
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

    

def clear_old_baskets():

    threshold = timezone.now() - timedelta(minutes=15) 
    Basket.objects.filter(created_at__lt=threshold).delete()


class BasketDeleteView(View):
    def post(self, request, slug_company, slug_username, item_id):
        session_key = request.session.session_key
        if session_key:
            # Удаляем только ту корзину, которая принадлежит текущему пользователю
            Basket.objects.filter(session_key=session_key, id=item_id).delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))
    




class SuccessView(ListView):
    model = SuccessModel
    template_name = 'client_web/success.html'
    context_object_name = 'success_entries'

    def get_queryset(self):
        session_key = self.request.session.session_key
        if not session_key:
            return SuccessModel.objects.none()
        return SuccessModel.objects.filter(session_key=session_key).select_related('name', 'executor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_entry = self.get_queryset().last()

        if last_entry:
            context["user"] = last_entry.name
            context["basket_items"] = last_entry.basket_history
            context["time_slot"] = last_entry.time_slot  # Добавляем временной слот в контекст
        else:
            print("No entries found in SuccessModel.")  # Отладочная информация

        return context
    
    






class ScheduleView(CreateView):
    template_name = 'client_web/client_schedule.html'
    model = ClientSchedule
    form_class = ClientScheduleForm
    success_url = reverse_lazy('client:user_form')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug_company'] = self.kwargs.get('slug_company')
        context['slug_username'] = self.kwargs.get('slug_username')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            date_id = request.GET.get("date")
            print(f"Received AJAX request for date ID: {date_id}")  # Отладочная информация
            if date_id:
                available_slots = TimeSlot.objects.filter(
                    schedule_id=date_id,
                    is_available=True
                ).values("id", "start_time", "end_time")
                print(f"Available slots: {list(available_slots)}")  # Отладочная информация
                return JsonResponse(list(available_slots), safe=False)
            return JsonResponse([], safe=False)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # Устанавливаем session_key
            form.instance.session_key = request.session.session_key

            # Получаем выбранные значения из формы
            selected_date = form.cleaned_data['select_day']
            selected_time_slot = form.cleaned_data['select_time']

            # Устанавливаем значения в экземпляр модели
            form.instance.date = selected_date
            form.instance.time_slot = selected_time_slot

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.executor = self.request.user  # Устанавливаем только для аутентифицированных пользователей
        form.instance.session_key = self.request.session.session_key
        response = super().form_valid(form)
        return redirect("client:user_form", slug_company=self.kwargs["slug_company"], slug_username=self.kwargs["slug_username"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('client:user_form', kwargs={
            'slug_company': self.kwargs['slug_company'],
            'slug_username': self.kwargs['slug_username']
        })
    
    



class UserFormView(CreateView): 
    model = UserForm
    form_class = UserBlank
    template_name = 'client_web/user_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        executor = get_object_or_404(User, username=self.kwargs["slug_username"])
        context["schedules"] = DaySchedule.objects.filter(
            is_working_day=True,
            calendar__owner=executor
        )
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.create()
            session_key = self.request.session.session_key

        basket = Basket.objects.filter(session_key=session_key).first()
        if not basket or basket.quantity == 0:  
            return redirect("client:client_basket", slug_company=self.kwargs["slug_company"], slug_username=self.kwargs["slug_username"])
        
        form.instance.session_key = session_key  
        user_form = form.save()
        
        executor = get_object_or_404(User, username=self.kwargs["slug_username"])
        basket_history = self._serialize_basket(basket)

        # Получаем последнюю запись из ClientSchedule
        client_schedule = ClientSchedule.objects.filter(
            session_key=session_key
        ).last()

        # Создаем запись в SuccessModel
        success_record = SuccessModel.objects.create(
            name=user_form,
            executor=executor,
            session_key=session_key,
            basket_history=basket_history,
            time_history={
                "selected_date": str(client_schedule.date.date) if client_schedule and client_schedule.date else None,
                "selected_time_slot": f"{client_schedule.time_slot.start_time} - {client_schedule.time_slot.end_time}" if client_schedule and client_schedule.time_slot else None,
            }
        )

        basket.delete()

        if self.request.session.session_key:
            self.request.session.flush()  # Удаляем текущую сессию
        self.request.session.create()  # Создаем новую сессию

        # Добавляем сообщение об успехе
        messages.success(self.request, "Запись успешно создана!")

        return super().form_valid(form)

    def _serialize_basket(self, basket):

        basket_items = Basket.objects.filter(session_key=basket.session_key)
        return [
            {
                "service": item.service.name,
                "quantity": item.quantity,
                "price": str(item.service.price),  # Преобразуем цену в строку для JSON
            }
            for item in basket_items
        ]

    def get_success_url(self):
        return reverse_lazy(
            'client:success', 
            kwargs={
                "slug_company": self.kwargs["slug_company"],
                "slug_username": self.kwargs["slug_username"],
            }
        )