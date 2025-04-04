from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from schedule.models import BusinessCalendar, DaySchedule, TimeSlot
from schedule.forms import DayScheduleForm, TimeSlotForm
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View


@login_required
def calendar_view(request):
    """Отображение календаря пользователя."""

    # Создаем календарь, если он еще не существует
    calendar, created = BusinessCalendar.objects.get_or_create(owner=request.user)

    schedules = DaySchedule.objects.filter(calendar=calendar).order_by('date')
    # print("Schedules:", schedules)  # Отладочная информация
    return render(request, 'schedule/calendar.html', {'schedules': schedules})


@login_required
def edit_schedule(request, pk):
    """Редактирование расписания дня."""
    if not request.user.is_staff:
        return render(request, 'schedule/error.html', {'message': 'Доступ запрещен'})

    schedule = get_object_or_404(DaySchedule, id=pk, calendar__owner=request.user)

    if request.method == 'POST':
        form = DayScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule:calendar')  # Используйте пространство имен
    else:
        form = DayScheduleForm(instance=schedule)

    # Получаем временные слоты для этого расписания
    time_slots = schedule.time_slots.all()

    return render(request, 'schedule/edit_schedule.html', {
        'form': form,
        'schedule': schedule,
        'time_slots': time_slots  # Передаем временные слоты в шаблон
    })





class CreateDay(LoginRequiredMixin, CreateView):
    template_name = "schedule/create_day.html"
    model = DaySchedule
    fields = ['date', 'is_working_day']
    success_url = reverse_lazy('schedule:calendar')

    def form_valid(self, form):
        user = self.request.user
        calendar = get_object_or_404(BusinessCalendar, owner=user)

        # Проверяем, существует ли уже расписание для этой даты
        if DaySchedule.objects.filter(calendar=calendar, date=form.cleaned_data['date']).exists():
            messages.error(self.request, 'Расписание для этой даты уже существует.')
            return super().form_invalid(form)

        # Привязываем расписание к календарю пользователя и устанавливаем owner и executor
        form.instance.calendar = calendar
        form.instance.owner = user  # Устанавливаем текущего пользователя как owner
        form.instance.executor = user  # Устанавливаем текущего пользователя как executor

        messages.success(self.request, 'Расписание успешно создано.')
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        date = self.request.GET.get('date')
        if date:
            initial['date'] = date
        return initial
    
class WorkDayDelete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        schedule = get_object_or_404(DaySchedule, pk=kwargs["pk"], calendar__owner=request.user)
        print(f"Deleting schedule: {schedule}")  # Отладочная информация
        schedule.delete()
        messages.success(request, 'Расписание успешно удалено.')
        return redirect('schedule:calendar')


class EditDayView(LoginRequiredMixin, UpdateView):

    model = DaySchedule
    fields = ['date', 'is_working_day']
    template_name = 'schedule/edit-day.html'
    success_url = reverse_lazy('calendar')

    def form_valid(self, form):
        messages.success(self.request, 'Расписание успешно обновлено.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule = self.get_object()
        context['time_slots'] = schedule.time_slots.all()  # Получаем все временные слоты для этого дня
        return context


@login_required
def edit_time_slot(request, pk):
    time_slot = get_object_or_404(TimeSlot, id=pk, schedule__calendar__owner=request.user)

    if request.method == 'POST':
        form = TimeSlotForm(request.POST, instance=time_slot)
        if form.is_valid():
            form.save()
            messages.success(request, 'Временной слот успешно обновлен.')
            return redirect('schedule:edit_schedule', pk=time_slot.schedule.id)
    else:
        form = TimeSlotForm(instance=time_slot)

    return render(request, 'schedule/edit_time_slot.html', {'form': form, 'time_slot': time_slot})


@login_required
def delete_time_slot(request, pk):
    time_slot = get_object_or_404(TimeSlot, id=pk, schedule__calendar__owner=request.user)
    schedule_id = time_slot.schedule.id
    time_slot.delete()
    messages.success(request, 'Временной слот успешно удален.')
    return redirect('schedule:edit_schedule', pk=schedule_id)