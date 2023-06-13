from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from apps.users.forms import CustomUserCreationForm, ProfileForm, TaskForm, Task, NewsForm, CustomUserChangeForm, SubnetForm
from apps.users.models import Notification, Profile, News, CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.forms import ValidationError
from django.utils import timezone
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.decorators import method_decorator
from .models import Subnet, IPAddress, Organization
from .forms import IPAddressForm
from django.db.models import Q

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'password/password_reset_done.html'
    email_template_name = 'password/password_reset.html'
    success_url = reverse_lazy('password_reset_done')

# Представление для подтверждения сброса пароля
class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

# Представление для успешного завершения сброса пароля
class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password/password_reset_complete.html'


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Сброс пароля"
                    email_template_name = "password/reset_password_email.html"
                    c = {
                        "email": user.email,
                        "domain": get_current_site(request).domain,
                        "site_name": "RcairSite",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    send_mail(subject, email, "RcairSite@yandex.ru", [user.email], fail_silently=False)
                return redirect("password_reset_done")
            else:
                form.add_error('email', 'Учетная запись с таким адресом электронной почты не существует')
    else:
        form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"form": form})



class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.user = CustomUser.objects.get(user=request.user)
        else:
            request.user = None


class ProfileView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        profile = request.user.profile
        tasks = Task.objects.filter(user=request.user)
        notifications = Notification.objects.filter(user=request.user)
        return render(request, 'users/profile.html', {'profile': profile, 'tasks': tasks, 'notifications': notifications})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request, 'users/profile.html', {'form': form})






class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('homepage')
    template_name = 'employee/employee_create.html'
    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Создание профиля и связь с пользователем
            profile = Profile(user=user)
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.telegram = form.cleaned_data['telegram']
            profile.team = form.cleaned_data['team']
            profile.project = form.cleaned_data['project']
            profile.save()

            logout(request)

            # Authenticate and login user after registration
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)

            return redirect('homepage')
        else:
            return render(request, self.template_name, {'form': form})
    def form_valid(self, form):
        response = super().form_valid(form)

        # Заполнение профиля данными из формы регистрации
        profile = self.object.profile
        profile.first_name = self.object.first_name
        profile.last_name = self.object.last_name
        profile.telegram = self.object.telegram
        profile.team = self.object.team
        profile.project = self.object.project
        profile.save()

        return response


class LoginView(LoginView):
    template_name = 'users/login.html'

    # Redirect from login page in case user already authenticated and loggedin
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('homepage')
        return self.render_to_response(self.get_context_data())


def complete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.completed = True
        task.save()
        return JsonResponse({'message': 'Task completed successfully'})

class TaskCreateView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'users/task_create.html', {'form': form})
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('profile')
        else:
            messages.error(request, 'Заполните необходимые поля.')
            return render(request, 'users/task_create.html', {'form': form})


class TaskDetailView(View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(instance=task)
        return render(request, 'users/task_edit.html', {'task': task, 'form': form})
    
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            # Проверка на изменение полей
            if form.has_changed():
                # Проверка на пустые поля
                if form.cleaned_data['title'] and form.cleaned_data['text']:
                    # Проверка даты дедлайна
                    deadline = form.cleaned_data['deadline']
                    if deadline < timezone.now():
                        form.add_error('deadline', 'Дедлайн не может быть в прошлом.')
                    else:
                        # Проверка времени напоминания
                        reminder_time = form.cleaned_data['reminder_time']
                        if reminder_time and reminder_time < timezone.now():
                            form.add_error('reminder_time', 'Время напоминания не может быть в прошлом.')
                        else:
                            form.save()
                            return redirect('task_edit', task_id=task_id)
                else:
                    form.add_error(None, "Поля не могут быть пустыми.")
            else:
                form.add_error(None, "Нет изменений в задаче.")
        return render(request, 'users/task_edit.html', {'task': task, 'form': form})

    



class TaskDeleteView(View):
    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect('profile')
    


#News
@login_required
def news(request):
    news = News.objects.all().order_by('-date_published')
    return render(request, 'news/news_list.html', {'news': news})

#News_Create
@login_required
def news_create(request):
    form = NewsForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        news = form.save(commit=False)
        news.author = request.user
        news.save()
        return redirect('news')
    return render(request, 'news/news_form.html', {'form': form})

#News_Edit
@login_required
def news_edit(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news_item)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, 'Новость успешно сохранена.')
            else:
                messages.error(request, 'Текст новости не был изменен.')
        else:
            messages.error(request, 'Поле должно быть заполнено')
    else:
        form = NewsForm(instance=news_item)
    
    context = {'form': form}
    return render(request, 'news/news_edit.html', context)

#News_Delete
@login_required
def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.delete()
    return redirect('news')

@login_required
def mark_news_read(request, notification_id):
    if request.method == 'POST':
        # Найти уведомление по его ID и текущему пользователю
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Уведомление не найдено'})

        # Отметить уведомление как прочитанное
        notification.is_read = True
        notification.save()

        # Удалить уведомление из списка уведомлений пользователя
        notification.delete()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Некорректный метод запроса'})


@login_required
def employee_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
        else:
            print(form.errors)  # Отладочный вывод ошибок формы
    else:
        form = CustomUserCreationForm()
    return render(request, 'employee/employee_create.html', {'form': form})




@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = CustomUserChangeForm(instance=employee)
    return render(request, 'employee/employee_edit.html', {'form': form, 'employee': employee})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee/employee_delete.html', {'employee': employee})

@login_required
def employee_list(request):
    employees = CustomUser.objects.all()
    return render(request, 'employee/employee_list.html', {'employees': employees})

@login_required
def subnet_list(request):
    subnets = Subnet.objects.all()
    search_query = request.GET.get('search')

    if search_query:
        subnets = subnets.filter(Q(name__icontains=search_query) | Q(network_address__icontains=search_query))

    return render(request, 'subnet/subnet_list.html', {'subnets': subnets})
@login_required
def subnet_detail(request, subnet_id):
    subnet = Subnet.objects.get(id=subnet_id)
    return render(request, 'subnet/subnet_detail.html', {'subnet': subnet})

@login_required
def subnet_create(request):
    if request.method == 'POST':
        form = SubnetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subnet_list')
        else:
            messages.error(request, '')
    else:
        form = SubnetForm()
    return render(request, 'subnet/subnet_create.html', {'form': form})

@login_required
def subnet_delete(request, subnet_id):
    subnet = get_object_or_404(Subnet, id=subnet_id)
    if request.method == 'POST':
        subnet.delete()
        return redirect('subnet_list')
    return render(request, 'subnet/subnet_delete.html', {'subnet': subnet})

@login_required
def ip_address_list(request, subnet_id):
    subnet = Subnet.objects.get(id=subnet_id)
    status = request.GET.get('status', 'all')

    if status == 'all':
        ip_addresses = IPAddress.objects.filter(subnet=subnet)
    elif status == 'free':
        ip_addresses = IPAddress.objects.filter(subnet=subnet, status='free')
    elif status == 'occupied':
        ip_addresses = IPAddress.objects.filter(subnet=subnet, status='occupied')
    else:
        # Обработка некорректного значения статуса, например, возвращение всех IP-адресов
        ip_addresses = IPAddress.objects.filter(subnet=subnet)

    context = {
        'ip_addresses': ip_addresses,
        'status': status,
    }
    return render(request, 'ipaddress/ip_address_list.html', context)

@login_required
def ip_address_detail(request, ip_address_id):
    ip_address = IPAddress.objects.get(id=ip_address_id)
    return render(request, 'ipaddress/ip_address_detail.html', {'ip_address': ip_address})

@login_required
def ip_address_create(request):
    if request.method == 'POST':
        form = IPAddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ip_address_list')
    else:
        form = IPAddressForm()
    return render(request, 'ipaddress/ip_address_create.html', {'form': form})

@login_required
def organization_list(request):
    organizations = Organization.objects.all()
    return render(request, 'organization/organization_list.html', {'organizations': organizations})

@login_required
def organization_detail(request, organization_id):
    organization = Organization.objects.get(id=organization_id)
    return render(request, 'organization/organization_detail.html', {'organization': organization})


