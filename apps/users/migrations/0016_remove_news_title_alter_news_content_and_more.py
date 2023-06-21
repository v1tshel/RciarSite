# Generated by Django 4.1.5 on 2023-06-19 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_news_content_alter_news_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='title',
        ),
        migrations.AlterField(
            model_name='news',
            name='content',
            field=models.TextField(max_length=300, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='news',
            name='date_published',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Содержимое новости'),
        ),
    ]
