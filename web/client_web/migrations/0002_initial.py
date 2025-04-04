# Generated by Django 5.1.7 on 2025-03-29 14:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client_web', '0001_initial'),
        ('schedule', '0001_initial'),
        ('services', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='executor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='basket',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.servicemodel'),
        ),
        migrations.AddField(
            model_name='clientschedule',
            name='date',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule.dayschedule'),
        ),
        migrations.AddField(
            model_name='clientschedule',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clientschedule',
            name='time_slot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedule.timeslot'),
        ),
        migrations.AddField(
            model_name='successmodel',
            name='executor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='successmodel',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client_web.userform'),
        ),
    ]
