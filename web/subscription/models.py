from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now


class TemporarySubscription(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True)
    subscription_type = models.CharField(max_length=50)         
    start_date = models.DateTimeField(auto_now_add=True)       
    end_date = models.DateTimeField()                        
    is_active = models.BooleanField(default=True) 
    
    class Meta: 
        verbose_name = "TemporarySubscription"
        verbose_name_plural = "TemporarySubscriptions"

        