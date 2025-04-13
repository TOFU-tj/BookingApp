from celery import shared_task
from subscription.models import TemporarySubscription
from django.utils import timezone

@shared_task
def update_subscription_statuses():
    """
    Периодическая задача для обновления статусов подписок.
    """
    subscriptions = TemporarySubscription.objects.filter(is_active=True)
    for subscription in subscriptions:
        if subscription.is_expired():
            subscription.is_active = False
            subscription.save()