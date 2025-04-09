from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from user.forms import UserLogInForm, UserRegistrationForm
from django.contrib import auth
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from user.models import User
from subscription.models import TemporarySubscription
from django.shortcuts import render, redirect
from django.contrib.auth import login

class UserLogIn(LoginView): 
    template_name = 'user/login.html'
    form_class = UserLogInForm 
    
    
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
                is_active=True
            )

            # Создаем пользователя
            user = form.save(commit=False)
            user.subscription = temp_subscription
            user.is_staff = True
            user.save()

            # Деактивируем временную подписку
            temp_subscription.is_active = False
            temp_subscription.save()

            # Авторизуем пользователя
            login(self.request, user)

            return redirect(self.success_url)

        except TemporarySubscription.DoesNotExist:
            return render(self.request, 'user/registration.html', {
                'error': 'Подписка не найдена или уже использована.'
            })