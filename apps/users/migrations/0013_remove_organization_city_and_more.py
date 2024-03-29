# Generated by Django 4.1.5 on 2023-06-08 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_ipaddress_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='city',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='numberhouse',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='street',
        ),
        migrations.CreateModel(
            name='OrganizationAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('numberhouse', models.CharField(max_length=50)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_addresses', to='users.organization')),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='addresses',
            field=models.ManyToManyField(through='users.OrganizationAddress', to='users.organization'),
        ),
        migrations.AlterField(
            model_name='ipaddress',
            name='organization_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.organizationaddress'),
        ),
    ]
