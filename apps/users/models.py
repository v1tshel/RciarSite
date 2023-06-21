from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator







class CustomUser(AbstractUser):
    GENDERS = (
        ('m', 'Мужчина'),
        ('f', 'Женщина'),
    )

   
    

    middle_name = models.CharField('Отчество', max_length=30, blank=True, default='')
    gender      = models.CharField('Пол', max_length=1, choices=GENDERS, default='')
    birth_date  = models.DateField('Дата рождения', default='2000-09-12')
    telegram    = models.CharField('Телеграм', max_length=30, blank=True, default='')
    team        = models.CharField('Команда', max_length=30, blank=True, default='')
    project     = models.CharField('Проект сотрудника', max_length=30, blank=True, default='')



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    telegram = models.CharField(max_length=30)
    team = models.CharField(max_length=30)
    project = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    profile, created = Profile.objects.get_or_create(user=instance)
    profile.first_name = instance.first_name
    profile.last_name = instance.last_name
    profile.email = instance.email
    profile.team = instance.team
    profile.project = instance.project
    profile.telegram = instance.telegram
    profile.save()


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Task(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField(max_length=300)
    deadline = models.DateTimeField()
    completed = models.BooleanField(default=False)
    reminder_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=100, default='')
    content = models.TextField(max_length=500)
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True, blank=True)
    task_reminder_time = models.DateTimeField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.news.title}"

    def is_task_due_soon(self):
        if self.task_reminder_time:
            return self.task_reminder_time <= timezone.now()
        return False

    
@receiver(post_save, sender=News)
def send_notification(sender, instance, created, **kwargs):
    if created:
        users = CustomUser.objects.all()
        for user in users:
            Notification.objects.create(user=user, news=instance)

class Subnet(models.Model):
    name = models.CharField(max_length=100)
    network_address = models.GenericIPAddressField(protocol='IPv4')
    subnet_mask = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(32)])

    def __str__(self):
        return self.name

class Organization(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    addresses = models.ManyToManyField('self', through='OrganizationAddress', symmetrical=False)

    def __str__(self):
        return self.name

class OrganizationAddress(models.Model):
    organization = models.ForeignKey(Organization, verbose_name='Организация', on_delete=models.CASCADE, related_name='organization_addresses')
    city = models.CharField(verbose_name='Город', max_length=50)
    street = models.CharField(verbose_name='Улица', max_length=50)
    numberhouse = models.CharField(verbose_name='Номер дома', max_length=5)

    def __str__(self):
        return f'{self.city}, {self.street}, {self.numberhouse}'

class IPAddress(models.Model):
    STATUS_CHOICES = (
        ('free', 'Свободен'),
        ('occupied', 'Занят'),
    )

    subnet = models.ForeignKey('Subnet', verbose_name='Подсеть', on_delete=models.CASCADE)
    address = models.GenericIPAddressField(verbose_name='IP-адрес', protocol='IPv4')
    status = models.CharField(verbose_name='Статус', max_length=10, choices=STATUS_CHOICES, default='free')
    organization = models.ForeignKey('Organization', verbose_name='Организация', on_delete=models.SET_NULL, null=True)
    organization_address = models.ForeignKey('OrganizationAddress', verbose_name='Адрес организации', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.address

    

