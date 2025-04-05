from celery import shared_task
from user.models import User
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

@shared_task
def check_subscriptions():
    users = User.objects.all()
    for user in users:
        try:
            if user.is_subscription_expired():
                if user.subscription.end_date + timezone.timedelta(days=10) < timezone.now():
                    logger.info(f"Deleting user: {user.username}")
                    user.delete_if_subscription_expired()
                else:
                    logger.info(f"Extending grace period for user: {user.username}")
                    user.extend_grace_period()
        except Exception as e:
            logger.error(f"Error processing user {user.username}: {e}")