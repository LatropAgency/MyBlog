from django.shortcuts import render, redirect
from .models import News, Comments
from django.contrib.auth.models import User
from .forms import commentForm, editPasswordForm, addNewsForm, UserInfoForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.generic import View, DetailView, ListView
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib import messages

count = 5


def index(request):
    page_num = 0
    query = list(reversed(get_list_or_404(News)))
    lst = reversed(query[page_num * count: (page_num + 1) * count:1])
    context = {'news': lst}
    if not (page_num + 1) * count >= len(query):
        context['forward'] = page_num + 1
    return render(request, 'index.html', context)


def page(request, page_num):
    query = list(reversed(get_list_or_404(News)))
    lst = reversed(query[page_num * count: (page_num + 1) * count:1])
    context = {'news': lst}
    if not page_num - 1 == -1:
        context['back'] = str(page_num - 1)
    if not (page_num + 1) * count >= len(query):
        context['forward'] = page_num + 1
    return render(request, 'index.html', context)


def details(request, news_id):
    query = get_object_or_404(News, pk=news_id)
    query.views = query.views + 1
    query.save()
    comment = commentForm()
    context = {"news_item": query}
    if request.user.has_perm('news.add_comments'):
        context["form"] = comment
    if request.method == "POST":
        comment = commentForm(request.POST)
        if comment.is_valid():
            comment = comment.cleaned_data
            new_comment = Comments(user_id=request.user.id, text=comment['text'], news_id=news_id)
            if request.user.has_perm('news.add_comments'):
                new_comment.save()
            return redirect(f'/{news_id}')
    return render(request, 'details.html', context)


@login_required(login_url='/auth/auth/')
def profile(request):
    context = {"group": request.user.groups.all(), 'info': UserInfoForm(), 'editPassword': editPasswordForm()}
    user = get_object_or_404(User, pk=request.user.id)
    if request.user.has_perm('news.add_news'):
        context['add_news'] = addNewsForm()
    if request.method == "POST":
        edit_password_form = editPasswordForm(request.POST)
        if edit_password_form.is_valid():
            edit_password_form = edit_password_form.cleaned_data
            if not (check_password(edit_password_form['old_password'], user.password)):
                messages.error(request, "Неверный пароль")
            else:
                user.set_password(edit_password_form['new_password'])
                user.save()
                messages.info(request, "Парль успешно изменён")
        else:
            for field in edit_password_form:
                for error in field.errors:
                    messages.error(request, error)
    return render(request, 'profile.html', context)


@permission_required('news.delete_comments', login_url='/error/')
def del_comment(request, news_id, comment_id):
    if request.user.has_perm('news.delete_comments'):
        Comments.objects.get(id=comment_id).delete()
        messages.info(request, "Комментарий успешно удалён")
        return redirect(f'/{news_id}')
    else:
        return redirect(f'/{news_id}')


@permission_required('auth.delete_group', login_url='/error/')
def mute(request, user_id):
    u = get_object_or_404(User, pk=user_id)
    if u.has_perm('news.add_comments'):
        g = Group.objects.get(name="Пользователь")
        g.user_set.remove(u)
        messages.info(request, "Пользователь успешно замучен")
        return render(request, 'details.html')
    else:
        return redirect('/')


@permission_required('auth.add_group', login_url='/error/')
def unmute(request, user_id):
    u = get_object_or_404(User, pk=user_id)
    if not u.has_perm('news.add_comments'):
        g = Group.objects.get(name="Пользователь")
        g.user_set.add(u)
        messages.info(request, "Пользователь успешно размучен")
        return render(request, 'details.html')
    else:
        return redirect('/')


@login_required(login_url='/auth/auth')
def add_editor(request, user_id):
    if request.user.is_superuser:
        u = get_object_or_404(User, pk=user_id)
        g = Group.objects.get(name="Редактор")
        g.user_set.add(u)
        messages.info(request, "Пользователю добавлены возможности редактора")
        return render(request, 'user.html')
    else:
        return redirect('/error/')


@login_required(login_url='/auth/auth/')
def add_moderator(request, user_id):
    if request.user.is_superuser:
        u = get_object_or_404(User, pk=user_id)
        g = Group.objects.get(name="Модератор")
        g.user_set.add(u)
        messages.info(request, "Пользователю добавлены возможности модератора")
        return render(request, 'user.html')
    else:
        return redirect('/error/')


@login_required(login_url='/auth/auth/')
def del_editor(request, user_id):
    if request.user.is_superuser:
        u = get_object_or_404(User, pk=user_id)
        g = Group.objects.get(name="Редактор")
        g.user_set.remove(u)
        messages.info(request, "Права редактора удалены")
        return render(request, 'user.html')
    else:
        return redirect('/error/')


@login_required(login_url='/auth/auth/')
def del_moderator(request, user_id):
    if request.user.is_superuser:
        u = get_object_or_404(User, pk=user_id)
        g = Group.objects.get(name="Модератор")
        g.user_set.remove(u)
        messages.info(request, "Права модератора удалены")
        return render(request, 'user.html')
    else:
        return redirect('/error/')


@permission_required('news.add_news', login_url='/error/')
def addNews(request):
    context = {}
    if request.method == "POST":
        add_news = addNewsForm(request.POST, request.FILES)
        if add_news.is_valid():
            add_news = add_news.cleaned_data
            ns = News(title=add_news['title'], text=add_news['text'], author_id=request.user.id,
                      image=add_news['image'], prev_text=add_news['prev_text'])
            ns.save()
            messages.info(request, "Новость опубликована")
    else:
        context["add_news"] = addNewsForm()
    return render(request, 'addnews.html', context)


@login_required(login_url='/auth/auth/')
def user_profile(request, user_id):
    usr = get_object_or_404(User, pk=user_id)
    group = usr.groups.all()
    return render(request, 'user.html', {'usr': usr, 'group': group})


def error(request):
    return render(request, 'error.html', {})
