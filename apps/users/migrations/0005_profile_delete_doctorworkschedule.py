# Generated by Django 4.1.5 on 2023-05-28 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_email_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('telegram', models.CharField(max_length=30)),
                ('team', models.CharField(max_length=30)),
                ('project', models.CharField(max_length=30)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile_photos')),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='DoctorWorkSchedule',
        ),
    ]
