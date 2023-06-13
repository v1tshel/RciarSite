from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Task
from apps.users.models import CustomUser, News, Notification, Subnet, IPAddress, Organization, OrganizationAddress
from apps.users.forms import CustomUserCreationForm, CustomUserChangeForm



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = []

    model = CustomUser
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm

    list_display = ['username', "first_name", "last_name", "email", 'telegram', 'team', 'project',
                    'email', 'gender', 'birth_date', 'is_staff']




    # Add user
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'middle_name',
                    'telegram',
                    'team',
                    'project',
                    'gender',
                    'birth_date',
                )
            }
        )
    )

    # Edit user
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'middle_name',
                    'telegram',
                    'team',
                    'project',
                    'gender',
                    'birth_date',
                )
            }
        )
    )

admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(News)
admin.site.register(Subnet)
admin.site.register(IPAddress)
admin.site.register(Organization)
admin.site.register(OrganizationAddress)







