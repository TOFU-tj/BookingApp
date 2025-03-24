from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from user.forms import UserLogInForm, UserRegistrationForm
from django.contrib import auth
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from user.models import User
from django.core.exceptions import ValidationError


class UserLogIn(LoginView): 
    template_name = 'user/login.html'
    form_class = UserLogInForm 
    
    
def logout(request): 
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
    
    
class UserRegistrations(CreateView):
    model = User
    template_name = 'user/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.is_staff = True
        self.object.save()
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)
    
