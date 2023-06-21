from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Profile, Task, News, IPAddress, Subnet, Organization, OrganizationAddress
from apps.users.models import CustomUser
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

def validate_not_empty(value):
    if not value:
        raise ValidationError('Это поле не может быть пустым.')

class CustomUserCreationForm(UserCreationForm):
    is_superuser = forms.BooleanField(label='Администратор', required=False)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    first_name = forms.CharField(label='Имя', max_length=30, validators=[validate_not_empty])
    last_name = forms.CharField(label='Фамилия', max_length=30, validators=[validate_not_empty])
    email = forms.CharField(label='Почта', max_length=254, validators=[validate_not_empty])
    telegram = forms.CharField(label='Телеграм', max_length=30, validators=[validate_not_empty])
    team = forms.CharField(label='Команда', max_length=30, validators=[validate_not_empty])
    project = forms.CharField(label='Проект', max_length=30, validators=[validate_not_empty])

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields +  ('username', 'first_name', 'last_name', 'middle_name', 'email', 'telegram', 'team', 'project', 
                  'gender', 'birth_date', 'password1', 'password2', 'is_superuser')

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином уже существует.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже существует.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return cleaned_data


class CustomUserChangeForm(UserChangeForm):

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            if len(password1) < 8:
                raise forms.ValidationError("Пароль должен содержать не менее 8 символов.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Пароли не совпадают.")
        return password2

    class Meta:
        model = CustomUser
        fields = ('username',  "first_name", "last_name", 'middle_name', "email", 'telegram', 'team', 'project', 
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


class NewsForm(forms.ModelForm):

    title = forms.CharField(label='Заголовок', max_length=100, validators=[MinLengthValidator(5)])
    content = forms.CharField(label='Содержимое новости', max_length=500, widget=forms.Textarea, validators=[MinLengthValidator(10)])

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
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(), label='Организация')
    city = forms.CharField(label='Город', validators=[MinLengthValidator(5)])
    street = forms.CharField(label='Улица', validators=[MinLengthValidator(3)])
    numberhouse = forms.CharField(label='Номер дома')

    class Meta:
        model = OrganizationAddress
        fields = ['organization', 'city', 'street', 'numberhouse']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтрация доступных организаций только для выбора
        self.fields['organization'].queryset = Organization.objects.all()

class IPAddressForm(forms.ModelForm):
    class Meta:
        model = IPAddress
        fields = ['subnet', 'address', 'status', 'organization', 'organization_address']