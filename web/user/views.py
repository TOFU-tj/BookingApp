from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from user.forms import UserLogInForm, UserRegistrationForm
from django.contrib import auth
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from user.models import User
from subscription.models import TemporarySubscription
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login



class UserLogIn(LoginView):
    template_name = 'user/login.html'
    form_class = UserLogInForm

    def form_valid(self, form):
        user = form.get_user()
        if user.subscription and user.subscription.is_expired():
            return redirect('subscription:subscription')  # Перенаправляем на страницу входа
        return super().form_valid(form)
    
def logout(request): 
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
    

class UserRegistrations(CreateView):
    template_name = "user/registration.html"
    form_class = UserRegistrationForm
    model = User
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        session_id = self.request.GET.get('session_id')
        if not session_id:
            return render(self.request, 'user/error.html', {
                'error': 'Подписка не оплачена. Пожалуйста, оплатите подписку.'
            })

        try:
            # Находим временную подписку
            temp_subscription = TemporarySubscription.objects.get(
                session_key=session_id,
                is_active=False
            )

            # Создаем пользователя
            user = form.save(commit=False)
            user.subscription = temp_subscription
            user.is_staff = True
            user.save()

            # Активируем временную подписку
            temp_subscription.is_active = True
            temp_subscription.save()

            return redirect(self.success_url)

        except TemporarySubscription.DoesNotExist:
            return render(self.request, 'user/registration.html', {
                'error': 'Подписка не найдена или уже использована.'
            })




def profile_view(request):
    user = request.user
    subscription = user.subscription

    # Обновляем статус подписки, если она существует
    if subscription:
        subscription.update_status()

    # Получаем данные для контекста
    context = {
        'user': user,
        'subscription_end_date': subscription.end_date.strftime('%d.%m.%Y') if subscription and subscription.is_active else "Нет активной подписки",
        'is_active': subscription.is_active if subscription else False,
    }

    return render(request, 'user/profile.html', context)