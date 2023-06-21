# Generated by Django 4.1.5 on 2023-06-19 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_news_title_alter_news_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='content',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='news',
            name='date_published',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]