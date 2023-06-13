from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Profile, Task, News, IPAddress, Subnet, Organization, OrganizationAddress
from apps.users.models import CustomUser



class CustomUserCreationForm(UserCreationForm):
    is_superuser = forms.BooleanField(label='Администратор', required=False)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'middle_name', 'email', 'telegram', 'team', 'project', 
                  'gender', 'birth_date', 'password1', 'password2', 'is_superuser')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', "first_name", "last_name", 'middle_name', "email", 'telegram', 'team', 'project', 
                  'gender', 'birth_date')




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'telegram', 'team', 'email', 'project', 'photo')



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'text', 'deadline', 'reminder_time']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'class': 'datetimepicker'}),
            'reminder_time': forms.DateTimeInput(attrs={'class': 'datetimepicker'}),
        }

#Блок для новостей
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'content') 



class SubnetForm(forms.ModelForm):

    name = forms.CharField(label='Название', widget=forms.TextInput)
    network_address = forms.CharField(label='IP-адрес', widget=forms.TextInput)
    subnet_mask = forms.CharField(label='Маска подсети', widget=forms.TextInput)

    class Meta:
        model = Subnet
        fields = ['name', 'network_address', 'subnet_mask']


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name']

class OrganizationAddressForm(forms.ModelForm):
    class Meta:
        model = OrganizationAddress
        fields = ['organization', 'city', 'street', 'numberhouse']

class IPAddressForm(forms.ModelForm):
    class Meta:
        model = IPAddress
        fields = ['subnet', 'address', 'status', 'organization', 'organization_address']