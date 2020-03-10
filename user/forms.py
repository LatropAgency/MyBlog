from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class authForm(forms.Form):
    login = forms.CharField(max_length=32,min_length=2, label = 'Логин')
    password = forms.CharField(widget=forms.PasswordInput,min_length=6, label = 'Пароль')


class regForm(forms.Form):
    email = forms.EmailField(required=True, label = 'E-mail')
    login = forms.CharField(max_length=32,min_length=2, label = 'Логин')
    password = forms.CharField(widget=forms.PasswordInput,min_length=6, label = 'Пароль')
    rep_password = forms.CharField(widget=forms.PasswordInput,min_length=6, label = 'Повторите пароль')

    def clean_email(self):
        data = self.cleaned_data
        if len(User.objects.filter(email=data['email'])) == 0:
            return data['email']
        else:
            raise ValidationError("Пользователь с такой почтой уже зарегистрирован")

    def clean_login(self):
        data = self.cleaned_data
        if len(User.objects.filter(username=data['login'])) == 0:
            return data['login']
        else:
            raise ValidationError("Пользователь с таким логином уже зарегистрирован")

    def clean_rep_password(self):
        data = self.cleaned_data
        if data['password']==data['rep_password']:
            return data['rep_password']
        else:
            raise ValidationError("Пароли не совпадают")


class forgetForm(forms.Form):
    username = forms.CharField(max_length=32,min_length=2, label = 'Логин')

    def clean_username(self):
        data = self.cleaned_data
        if len(User.objects.filter(username=data['username'])) == 1:
            return data['username']
        else:
            raise ValidationError("Такого пользователя нет")


class resetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,min_length=6, label = 'Пароль')
    rep_password = forms.CharField(widget=forms.PasswordInput,min_length=6, label = 'Повторите пароль')

    def clean_rep_password(self):
        data = self.cleaned_data
        if data['password']==data['rep_password']:
            return data['rep_password']
        else:
            raise ValidationError("Пароли не совпадают")
