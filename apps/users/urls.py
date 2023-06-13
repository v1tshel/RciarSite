from django.urls import path, include
from .views import TaskDeleteView, TaskDetailView
from django.conf import settings
from django.conf.urls.static import static
from . import views 

from apps.users.views import SignUpView, LoginView, ProfileView



urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path('task_create/', ProfileView.as_view(), name='task_create'),
    path('task_delete/<int:task_id>/', TaskDeleteView.as_view(), name='task_delete'),
    path('task_edit/<int:task_id>/', TaskDetailView.as_view(), name='task_edit'),
    path('task/<int:task_id>/complete', views.complete_task, name='task_complete'),
    path('mark_news_read/<int:notification_id>', views.mark_news_read, name='mark_news_read'),

    
    path('', include('django.contrib.auth.urls')),


    path('password/reset/', views.password_reset_request, name='password_reset'),

    # URL-шаблоны для представлений сброса пароля
    path('password/reset/done/', views.PasswordResetView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('news/', views.news, name='news'),
    path('news/create/', views.news_create, name='news_create'),
    path('<int:pk>/news/edit/', views.news_edit, name='news_edit'),
    path('<int:pk>/news/delete/', views.news_delete, name='news_delete'),

    path('employee/list', views.employee_list, name='employee_list'),
    path('employee/add/', views.employee_create, name='employee_create'),
    path('employee/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employee/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    

    path('subnets/list/', views.subnet_list, name='subnet_list'),
    path('subnets/<int:subnet_id>/', views.subnet_detail, name='subnet_detail'),
    path('subnets/create/', views.subnet_create, name='subnet_create'),
    path('subnets/<int:subnet_id>/delete/', views.subnet_delete, name='subnet_delete'),
    
    path('subnet/<int:subnet_id>/ipaddresses/', views.ip_address_list, name='ip_address_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

