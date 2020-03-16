from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class AvatarForm(forms.Form):
    image = forms.FileField(label='Аватар')

    def clean_image(self):
        data = self.cleaned_data
        print(data['image'])
        if not (data['image'].name.endswith('.gif') or data['image'].name.endswith('.jpg') or
                data['image'].name.endswith('.jpeg') or data['image'].name.endswith('.png')):
            raise ValidationError("Загружать можно только изображения. Поддерживаемые расширения: .gif/.png/.jpg/.jpeg")
        else:
            return data['image']


class authForm(forms.Form):
    login = forms.CharField(max_length=32, min_length=2, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Пароль')


class commentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Оставить комментарий')


class regForm(forms.Form):
    email = forms.EmailField(required=True, label='E-mail')
    login = forms.CharField(max_length=32, min_length=2, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Пароль')
    rep_password = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Повторите пароль')

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
        if data['password'] == data['rep_password']:
            return data['rep_password']
        else:
            raise ValidationError("Пароли не совпадают")


class editPasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Текущий пароль')
    new_password = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Новый пароль')
    rep_new_password = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Повторите пароль')

    def clean_rep_new_password(self):
        data = self.cleaned_data
        if data['rep_new_password'] == data['new_password']:
            if data['old_password'] != data['new_password']:
                return data['new_password']
            else:
                raise ValidationError("Нельзя изменить пароль на текущий")
        else:
            raise ValidationError("Пароли не совпадают")


class addNewsForm(forms.Form):
    title = forms.CharField(max_length=200, label='Заголовок')
    prev_text = forms.CharField(widget=forms.Textarea, label='Превью текст')
    text = forms.CharField(widget=forms.Textarea, label='Основной текст')
    image = forms.FileField(label='Изображение')

    def clean_image(self):
        data = self.cleaned_data
        if not (data['image'].name.endswith('.gif') or data['image'].name.endswith('.jpg') or
                data['image'].name.endswith('.jpeg') or data['image'].name.endswith('.png')):
            raise ValidationError("Загружать можно только изображения. Поддерживаемые расширения: .gif/.png/.jpg/.jpeg")
        else:
            return data['image']


class forgetForm(forms.Form):
    username = forms.CharField(max_length=32, min_length=2, label='Логин')


class resetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Пароль')
    rep_password = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Повторите пароль')

    def clean_rep_password(self):
        data = self.cleaned_data
        if data['password'] == data['rep_password']:
            return data['rep_password']
        else:
            raise ValidationError("Пароли не совпадают")
