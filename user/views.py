from .forms import AuthForm, RegForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required


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
            user = authenticate(request, username=auth_user['login'], password=auth_user['password'])
            if not user == None:
                login(request, user)
                return redirect('news:index')
            messages.error(request, "Пользователя с таким логином и паролем не найдено")
        else:
            print_messages(request, auth_user)
        return render(request, 'auth.html', {'signin': AuthForm()})


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
            user.save()
            messages.info(request, "Вы успешно зарегистрировались.")
        else:
            print_messages(request, reg_user)
        return render(request, 'reg.html', {'signup': RegForm()})


@login_required(login_url='user:auth')
def log_out(request):
    logout(request)
    return redirect('news:index')
