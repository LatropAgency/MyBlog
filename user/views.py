from .forms import AuthForm, RegForm, ForgetForm, ResetForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
import datetime
import hashlib
from django.core.mail import send_mail


def print_messages(request, errors):
    for field in errors:
        for error in field.errors:
            messages.error(request, error)


class AuthView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'auth.html', {'signin': AuthForm()})
        else:
            messages.error(request, "Вы уже авторизованы")
            return redirect('news:index')

    def post(self, request, *args, **kwargs):
        auth_user = AuthForm(request.POST)
        if auth_user.is_valid():
            auth_user = auth_user.cleaned_data
            try:
                u = User.objects.get(username=auth_user['login'])
                user = authenticate(request, username=auth_user['login'], password=auth_user['password'])
                if u.is_active:
                    login(request, user)
                    return redirect('news:index')
                else:
                    messages.error(request, "Активируйте аккаунт")
                    return render(request, 'auth.html', {'signin': AuthForm()})
            except:
                messages.error(request, "Пользователя с таким логином и паролем не найдено")
                return render(request, 'auth.html', {'signin': AuthForm()})

        else:
            print_messages(request, auth_user)


class RegView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'reg.html', {'signup': RegForm()})
        else:
            messages.error(request, "Вы уже авторизованы")
            return redirect('news:index')

    def post(self, request, *args, **kwargs):
        reg_user = RegForm(request.POST)
        if reg_user.is_valid():
            reg_user = reg_user.cleaned_data
            user = User.objects.create_user(reg_user['login'], reg_user['email'], reg_user['password'])
            g = Group.objects.get(name="Пользователь")
            g.user_set.add(user)
            hash = hashlib.sha1(user.username.encode('utf-8')).hexdigest()
            send_mail('Активация аккаунта', f'Нажмите: https://latropblog.herokuapp.com/user/activate/{hash}',
                      'csdmmaxplay@gmail.com', [user.email], False)
            user.is_active = False
            user.save()
            messages.info(request, "Вы успешно зарегистрировались.")
        else:
            print_messages(request, reg_user)
        return render(request, 'reg.html', {'signup': RegForm()})


@login_required(login_url='user:auth')
def log_out(request):
    logout(request)
    return redirect('news:index')


class ForgetView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'forget.html', {'forget': ForgetForm})
        else:
            messages.error(request, "Вы уже авторизованы")
            return redirect('news:index')

    def post(self, request, *args, **kwargs):
        user_form = ForgetForm(request.POST)
        if user_form.is_valid():
            user_form = user_form.cleaned_data
            user = User.objects.get(username=user_form['username'])
            hash = hashlib.sha1(user.username.encode('utf-8')).hexdigest()
            send_mail('Забыли пароль', f'Сбросить пароль: https://latropblog.herokuapp.com/user/reset/{hash}',
                      'csdmmaxplay@gmail.com', [user.email], False)
            messages.info(request, 'Проверьте почту')
        else:
            print_messages(request, user_form)
        return redirect('user:forget')


def reset(request, hashuser):
    if not request.user.is_authenticated:
        users = User.objects.filter()
        for user in users:
            if hashuser == hashlib.sha1(user.username.encode('utf-8')).hexdigest():
                if request.method == "POST":
                    reset = ResetForm(request.POST)
                    if reset.is_valid():
                        reset = reset.cleaned_data
                        user.set_password(reset['password'])
                        user.save()
                        messages.info(request, "Пароль успешно изменён")
                        return redirect('news:index')
                    else:
                        print_messages(request, reset)
                return render(request, 'reset.html', {'reset': ResetForm})
        else:
            return redirect('news:error404')
    else:
        messages.error(request, "Вы уже авторизованы")
        return redirect('news:index')


def activate(request, hashuser):
    if not request.user.is_authenticated:
        users = User.objects.filter(is_active=False)
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
