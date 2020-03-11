from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.base import View

from .forms import authForm, regForm, forgetForm, resetForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import hashlib
from django.shortcuts import get_object_or_404, get_list_or_404
import datetime
from django.contrib import messages
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def print_messages(request, errors):
    for field in errors:
        for error in field.errors:
            messages.error(request, error)


class AuthView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'auth.html', {'signin': authForm()})
        else:
            return redirect('/')

    def post(self, request, *args, **kwargs):
        auth_user = authForm(request.POST)
        if auth_user.is_valid():
            auth_user = auth_user.cleaned_data
            try:
                u = User.objects.get(username=auth_user['login'])
                user = authenticate(request, username=auth_user['login'], password=auth_user['password'])
                if u.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, "Активируйте аккаунт")
                    return render(request, 'auth.html', {'signin': authForm()})
            except:
                messages.error(request, "Пользователя с таким логином и паролем не найдено")
                return render(request, 'auth.html', {'signin': authForm()})

        else:
            print_messages(request, auth_user)


def auth(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            auth_user = authForm(request.POST)
            if auth_user.is_valid():
                auth_user = auth_user.cleaned_data
                user = authenticate(request, username=auth_user["login"], password=auth_user["password"])
                if user is not None:
                    if user.last_login == None:
                        messages.error(request, "Активируйте аккаунт")
                    elif user.is_active:
                        login(request, user)
                        return redirect('/')
                else:
                    messages.error(request, "Пользователя с таким логином и паролем не найдено")
                    return render(request, 'auth.html', {'signin': authForm()})
            else:
                print_messages(request, auth_user)
        else:
            return render(request, 'auth.html', {'signin': authForm()})
        return render(request, 'auth.html')
    else:
        messages.error(request, "Вы уже авторизованы")
        return render(request, 'auth.html')


def reg(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            reg_user = regForm(request.POST)
            if reg_user.is_valid():
                reg_user = reg_user.cleaned_data
                user = User.objects.create_user(reg_user['login'], reg_user['email'], reg_user['password'])
                g = Group.objects.get(name="Пользователь")
                g.user_set.add(user)
                hash = hashlib.sha1(user.username.encode('utf-8')).hexdigest()
                email = EmailMessage('Активация аккаунта', f'Нажмите: http://127.0.0.1:8000/user/activate/{hash}',
                                     to=[user.email])
                email.send()
                user.is_active = False
                user.save()
                messages.info(request, "Вы успешно зарегистрировались. Вам на почту отправлено письмо")
            else:
                print_messages(request, reg_user)
                return render(request, 'reg.html', {'signup': regForm()})
        else:
            return render(request, 'reg.html', {'signup': regForm()})
        return render(request, 'reg.html')
    else:
        messages.error(request, "Вы уже авторизованы")
        return render(request, 'reg.html')


@login_required(login_url='/auth')
def log_out(request):
    logout(request)
    return redirect('/')


def error(request):
    return render(request, 'error.html', {})


def forget(request):
    if request.method == "POST":
        user_form = forgetForm(request.POST)
        if user_form.is_valid():
            user_form = user_form.cleaned_data
            user = get_object_or_404(User, username=user_form['username'])
            hash = hashlib.sha1(user.username.encode('utf-8')).hexdigest()
            email = EmailMessage('Забыли пароль', f'Сбросить пароль: http://127.0.0.1:8000/user/reset/{hash}',
                                 to=[user.email])
            message = Mail(
                from_email='csdmmaxplay@gmail.com',
                to_emails='csdmmaxplay@gmail.com',
                subject='Sending with Twilio SendGrid is Fun',
                html_content='<strong>and easy to do anywhere, even with Python</strong>')
            try:
                sg = SendGridAPIClient('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')
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
                messages.info(request, 'Проверьте почту')
            except Exception as e:
                messages.error(request, e.message)
            #email.send()
        else:
            print_messages(request, user_form)
    else:
        return render(request, 'forget.html', {'forget': forgetForm})
    return render(request, 'forget.html')


def reset(request, hashuser):
    users = get_list_or_404(User)
    for user in users:
        if hashuser == hashlib.sha1(user.username.encode('utf-8')).hexdigest():
            if request.method == "POST":
                reset = resetForm(request.POST)
                if reset.is_valid():
                    reset = reset.cleaned_data
                    user.set_password(reset['password'])
                    user.save()
                    messages.info(request, "Пароль успешно изменён")
                    return render(request, 'reset.html')
                else:
                    print_messages(request, reset)
            return render(request, 'reset.html', {'reset': resetForm})
    else:
        return redirect('/')


def activate(request, hashuser):
    if not request.user.is_authenticated:
        users = get_list_or_404(User, is_active=False)
        for user in users:
            if hashuser == hashlib.sha1(user.username.encode('utf-8')).hexdigest():
                user.last_login = datetime.datetime.now()
                user.is_active = True
                user.save()
                messages.info(request, 'Аккаунт активирован')
                return render(request, 'activate.html')
        else:
            messages.error(request, 'Ошибка')
            return render(request, 'activate.html')
    else:
        messages.error(request, 'Вы уже авторизованы')
        return render(request, 'activate.html')
