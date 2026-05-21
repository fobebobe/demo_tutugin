import re
from django import forms
from django.contrib.auth.models import User
from .models import Profile, CourseApplication


class RegistrationForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        min_length=6,
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Латиница и цифры, не менее 6 символов'
        })
    )
    password = forms.CharField(
        label='Пароль',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Минимум 8 символов'
        })
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )
    full_name = forms.CharField(
        label='ФИО',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иванов Иван Иванович'
        })
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '8(XXX)XXX-XX-XX'
        })
    )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.ru'
        })
    )

    #валидацияя
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError('Логин должен содержать только латинские буквы и цифры.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[а-яА-ЯёЁ\s]+$', full_name):
            raise forms.ValidationError('ФИО должно содержать только кириллицу и пробелы.')
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', phone):
            raise forms.ValidationError('Телефон должен быть в формате: 8(XXX)XXX-XX-XX')
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Пароли не совпадают.')
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите логин'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class ApplicationForm(forms.ModelForm): #форма создания для заявки
    class Meta:
        model = CourseApplication
        fields = ['course', 'desired_date', 'payment_method']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'desired_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }


class ReviewForm(forms.Form):
    review = forms.CharField(
        label='Отзыв',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Напишите ваш отзыв о курсе...'
        })
    )


class StatusForm(forms.Form):
   #форма изменения статуса для заявки на админке
    status = forms.ChoiceField(
        label='Статус',
        choices=CourseApplication.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
