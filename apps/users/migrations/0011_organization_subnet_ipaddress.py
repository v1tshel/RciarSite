# Generated by Django 4.1.5 on 2023-06-08 14:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_notification_task_deadline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('numberhouse', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Subnet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('network_address', models.GenericIPAddressField(protocol='IPv4')),
                ('subnet_mask', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(32)])),
            ],
        ),
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.GenericIPAddressField(protocol='IPv4')),
                ('status', models.CharField(choices=[('free', 'Свободен'), ('occupied', 'Занят')], default='free', max_length=10)),
                ('organization', models.CharField(max_length=100)),
                ('organization_address', models.CharField(max_length=200)),
                ('subnet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.subnet')),
            ],
        ),
    ]