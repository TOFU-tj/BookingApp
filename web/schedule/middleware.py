from .models import DaySchedule

class DeletePastDaysMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Удаляем прошедшие дни
        DaySchedule.delete_past_days()
        response = self.get_response(request)
        return response

from django.utils import timezone
import pytz

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_timezone = request.COOKIES.get('user_timezone', 'UTC')
        if user_timezone in pytz.all_timezones:
            timezone.activate(pytz.timezone(user_timezone))
        else:
            timezone.deactivate()
        response = self.get_response(request)
        return response