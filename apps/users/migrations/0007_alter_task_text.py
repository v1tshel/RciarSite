# Generated by Django 4.1.5 on 2023-06-06 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='text',
            field=models.TextField(max_length=300),
        ),
    ]