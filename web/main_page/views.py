from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic import DeleteView
from django.urls import reverse, reverse_lazy
from client_web.models import SuccessModel
from main_page.forms import UserBlankForm
from main_page.tasks import send_email_task
from django.contrib.auth.decorators import login_required

class OrderViews( ListView):
    model = SuccessModel
    template_name = 'main_page/main.html'
    context_object_name = "records"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return SuccessModel.objects.filter(executor=self.request.user).select_related('name', 'executor')
        return SuccessModel.objects.none()  # Возвращаем пустой QuerySet для неаутентифицированных пользователей
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        records = self.get_queryset()
        context["records"] = records

        return context
    
    
class RecordDeleteView(DeleteView):
    model = SuccessModel
    template_name = 'main_page/record_confirm_delete.html'  
    context_object_name = 'record'

    def get_success_url(self):
        return reverse_lazy('main:order')

    def get_queryset(self):
        return SuccessModel.objects.filter(executor=self.request.user)


@login_required
def generate_client_service_link(request):
    user = request.user
    if user.is_authenticated and user.slug_company and user.slug_username:
    
        link = request.build_absolute_uri(reverse(
            'client:client_services', 
            kwargs={'slug_company': user.slug_company, 'slug_username': user.slug_username}
        ))
        return render(request, 'main_page/link.html', {'link': link})
    else:
        # If the necessary data is missing, return an error
        return render(request, 'main_page/link.html', {'error': 'Не удалось создать ссылку.'})




class MainPage(TemplateView):
    template_name = 'main_page/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserBlankForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = UserBlankForm(request.POST)
        if form.is_valid():
            user_blank = form.save()
            
            subject = f"Новая заявка от {user_blank.name}"
            message = f"Вы получили новую заявку от {user_blank.name}.\n\n" \
                      f"Email: {user_blank.email}\n" \
                      f"Комментарий: {user_blank.text}"
            recipient_list = ['dmustafo863@gmail.com']
            
            send_email_task.delay(subject, message, recipient_list)

            return redirect('main:success_page')
        else:
            return render(request, self.template_name, {'form': form}) 


class SuccessPage(TemplateView):
    template_name = 'main_page/success.html'
