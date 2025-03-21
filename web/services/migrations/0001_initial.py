# Generated by Django 5.1.6 on 2025-03-13 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('client_name', models.CharField(max_length=100)),
                ('client_phone', models.CharField(max_length=20)),
                ('is_confirmed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='service')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='price')),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='WorkSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_available', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Work Schedule',
                'verbose_name_plural': 'Work Schedules',
                'ordering': ['schedule_date', 'start_time'],
            },
        ),
    ]
