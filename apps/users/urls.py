from django.urls import path, include
from .views import TaskDeleteView, TaskDetailView, TaskCreateView
from django.conf import settings
from django.conf.urls.static import static
from . import views 


from apps.users.views import SignUpView, LoginView, ProfileView



urlpatterns = [


    path('accounts/login/', LoginView.as_view(), name='login'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path('task_create/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:task_id>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('mark_news_read/<int:notification_id>', views.mark_news_read, name='mark_news_read'),
    path('task_edit/<int:task_id>/', TaskDetailView.as_view(), name='task_edit'),
    path('task/<int:task_id>/complete', views.complete_task, name='task_complete'),
    

    
    path('', include('django.contrib.auth.urls')),


    path('password/reset/', views.password_reset_request, name='password_reset'),
    path('password/reset/done/', views.PasswordResetView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('organizations/', views.organization_list, name='organization_list'),
    path('organizations/create/', views.organization_create, name='organization_create'),
    path('<int:organization_id>/address/create/', views.address_create, name='address_create'),
    path('organizations/<int:pk>/edit/', views.organization_edit, name='organization_edit'),
    path('organizations/<int:pk>/delete/', views.organization_delete, name='organization_delete'),

    path('news/', views.news, name='news'),
    path('news/create/', views.news_create, name='news_create'),
    path('<int:pk>/news/edit/', views.news_edit, name='news_edit'),
    path('<int:pk>/news/delete/', views.news_delete, name='news_delete'),

    path('employee/list', views.employee_list, name='employee_list'),
    path('employee/add/', views.employee_create, name='employee_create'),
    path('employee/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employee/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    

    path('subnets/list/', views.subnet_list, name='subnet_list'),
    path('subnets/<int:pk>/', views.subnet_detail, name='subnet_detail'),
    path('subnets/create/', views.subnet_create, name='subnet_create'),
    path('subnets/<int:subnet_id>/delete/', views.subnet_delete, name='subnet_delete'),
    
    path('subnets/<int:subnet_id>/ip_adress/', views.ip_address_list, name='ip_address_list'),
    path('subnets/ip_adress/create', views.ip_address_create, name='ip_adress_create'),
    path('subnets/ip_adress/<int:pk>/', views.ip_address_detail, name='ip_address_detail'),
    path('subnets/ip_adress/<int:ip_address_id>/delete/', views.ip_address_delete, name='ip_address_delete'),

    path('save_avatar/', views.SaveProfileView.as_view(), name='save_avatar'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

