# Generated by Django 4.1.5 on 2023-06-07 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_news_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date_published',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
