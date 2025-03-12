# Generated by Django 5.1.6 on 2025-03-12 14:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client_web', '0002_initial'),
        ('services', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='successmodel',
            name='executor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userform',
            name='Basket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client_web.basket'),
        ),
        migrations.AddField(
            model_name='userform',
            name='select_schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.workschedule'),
        ),
        migrations.AddField(
            model_name='successmodel',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client_web.userform'),
        ),
    ]
