from django.contrib.auth.views import LoginView
from user.forms import UserLogInForm
from django.contrib import auth
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


class UserLogIn(LoginView): 
    template_name = 'user/login.html'
    form_class = UserLogInForm 
    
def logout(request): 
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
    