from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from user.forms import UserLogInForm, UserRegistrationForm
from django.contrib import auth
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from user.models import User
from django.core.exceptions import ValidationError
from subscription.models import TemporarySubscription

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
        response = super().form_valid(form)
        self.object.is_staff = True
        self.object.save()

        # Получаем session_id из GET-параметров
        session_id = self.request.GET.get('session_id')
        if session_id:
            try:
                # Находим временную подписку
                temp_subscription = TemporarySubscription.objects.get(session_key=session_id)

                # Привязываем подписку к пользователю
                self.object.subscription = temp_subscription
                self.object.save()

                # Обновляем статус подписки
                temp_subscription.is_active = False
                temp_subscription.save()
            except TemporarySubscription.DoesNotExist:
                pass

        return response

    def form_invalid(self, form):
        return super().form_invalid(form)