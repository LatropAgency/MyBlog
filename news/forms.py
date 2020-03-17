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


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Оставить комментарий')


class EditPasswordForm(forms.Form):
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


class AddNewsForm(forms.Form):
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
