from celery import shared_task
from user.models import User
import logging
from django.utils import timezone



logger = logging.getLogger(__name__)

@shared_task
def check_subscriptions():
    """
    Периодическая задача для проверки подписок.
    Удаляет пользователей с истекшей подпиской.
    """
    users = User.objects.all()

    for user in users:
        logger.info(f"Checking subscription for user: {user.username}")
        if user.subscription and user.subscription.is_expired():
            user.delete_if_subscription_expired()
            logger.info(f"Deleted user due to expired subscription: {user.username}")