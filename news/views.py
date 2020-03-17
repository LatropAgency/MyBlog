from .models import News, Comments
from .forms import CommentForm, EditPasswordForm, AddNewsForm, AvatarForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group

COUNT = 4


def print_messages(request, errors):
    for field in errors:
        for error in field.errors:
            messages.error(request, error)


def index(request):
    page_num = 0
    query = list(reversed(News.objects.filter()))
    if not request.user.has_perm('news.view_hidden_news'):
        query = [item for item in query if not item.hidden]
    lst = reversed(query[page_num * COUNT: (page_num + 1) * COUNT:1])
    context = {'news': lst}
    if not (page_num + 1) * COUNT >= len(query):
        context['forward'] = page_num + 1
    return render(request, 'index.html', context)


def page(request, page_num):
    query = list(reversed(News.objects.filter()))
    if not request.user.has_perm('news.view_hidden_news'):
        query = [item for item in query if not item.hidden]
    lst = reversed(query[page_num * COUNT: (page_num + 1) * COUNT:1])
    context = {'news': lst}
    if not page_num - 1 == -1:
        context['back'] = str(page_num - 1)
    if not (page_num + 1) * COUNT >= len(query):
        context['forward'] = page_num + 1
    return render(request, 'index.html', context)


class NewsDetailsView(View):
    def get(self, request, *args, **kwargs):
        try:
            news_item = News.objects.get(id=kwargs['news_id'])
        except:
            return redirect('news:error404')
        if news_item.hidden:
            if not request.user.has_perm('news.view_hidden_news'):
                return redirect('news:error404')
        news_item.views = news_item.views + 1
        news_item.save()
        return render(request, 'details.html', {"news_item": news_item, 'form': CommentForm()})

    def post(self, request, *args, **kwargs):
        if request.user.has_perm('news.add_comments'):
            comment = CommentForm(request.POST)
            if comment.is_valid():
                comment = comment.cleaned_data
                new_comment = Comments(user_id=request.user.id, text=comment['text'], news_id=kwargs['news_id'])
                new_comment.save()
        else:
            messages.error(request, 'Вы не можете оставлять комментарии')
        return redirect('news:details', kwargs['news_id'])


@login_required(login_url='user:auth')
def change_avatar(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        avatar_form = AvatarForm(request.POST, request.FILES)
        if avatar_form.is_valid():
            avatar_form = avatar_form.cleaned_data
            user.extended.avatar = avatar_form['image']
            user.save()
            messages.info(request, 'Изображение успешно загружено')
        else:
            print_messages(request, avatar_form)
    return redirect('news:profile')


@login_required(login_url='user:auth')
def change_password(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        username = user.username
        edit_password_form = EditPasswordForm(request.POST)
        if edit_password_form.is_valid():
            edit_password_form = edit_password_form.cleaned_data
            if not (check_password(edit_password_form['old_password'], user.password)):
                messages.error(request, "Неверный пароль")
            else:
                user.set_password(edit_password_form['new_password'])
                user.save()
                messages.info(request, "Пароль успешно изменён")
                user = authenticate(request, username=username, password=edit_password_form['new_password'])
                login(request, user)
        else:
            print_messages(request, edit_password_form)
    return redirect('news:profile')


@login_required(login_url='user:auth')
def profile(request):
    return render(request, 'profile.html',
                  {"group": request.user.groups.all(), 'edit_password': EditPasswordForm(),
                   'avatar': AvatarForm()})


@permission_required('news.hide_news', login_url='news:error')
def hide_news(request, news_id):
    try:
        news_item = News.objects.get(id=news_id)
    except:
        return redirect('news:error404')
    if news_item.hidden:
        messages.info(request, "Новость успешно показана")
    else:
        messages.info(request, "Новость успешно скрыта")
    news_item.hidden = not news_item.hidden
    news_item.save()
    return redirect('news:index')


@permission_required('news.edit_news', login_url='news:error')
def edit_news(request, news_id):
    if request.method == "POST":
        news = AddNewsForm(request.POST, request.FILES)
        if news.is_valid():
            news = news.cleaned_data
            ns = News.objects.get(id=news_id)
            ns.text = news['text']
            ns.title = news['title']
            ns.prev_text = news['prev_text']
            ns.image = news['image']
            ns.save()
            messages.info(request, "Новость изменена")
        else:
            print_messages(request, news)
    news = News.objects.get(id=news_id)
    edit_form = AddNewsForm(
        initial={'title': news.title, 'text': news.text, 'prev_text': news.prev_text, 'image': news.image})
    return render(request, 'edit_news.html', {'edit_news': edit_form})


@permission_required('news.delete_news', login_url='news:error')
def del_news(request, news_id):
    try:
        News.objects.get(id=news_id).delete()
    except:
        return redirect('news:error404')
    messages.info(request, "Новость успешно удалёна")
    return redirect('news:index')


@permission_required('news.delete_comments', login_url='news:error')
def del_comment(request, news_id, comment_id):
    try:
        Comments.objects.get(id=comment_id).delete()
    except:
        return redirect('news:error404')
    messages.info(request, "Комментарий успешно удалён")
    return redirect(f'/{news_id}')


@permission_required('auth.mute', login_url='news:error')
def mute(request, user_id):
    try:
        u = User.objects.get(id=user_id)
    except:
        return redirect('news:error404')
    if u.has_perm('news.add_comments'):
        g = Group.objects.get(name="Пользователь")
        g.user_set.remove(u)
        messages.info(request, "Пользователь успешно замучен")
    return redirect('news:user', user_id)


@permission_required('auth.unmute', login_url='news:error')
def unmute(request, user_id):
    try:
        u = User.objects.get(id=user_id)
    except:
        return redirect('news:error404')
    if not u.has_perm('news.add_comments'):
        g = Group.objects.get(name="Пользователь")
        g.user_set.add(u)
        messages.info(request, "Пользователь успешно размучен")
    return redirect('news:user', user_id)


@permission_required('auth.add_group', login_url='news:error')
def add_editor(request, user_id):
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=user_id)
        except:
            return redirect('news:error404')
        group = Group.objects.get(name="Редактор")
        group.user_set.add(user)
        messages.info(request, "Пользователю добавлены возможности редактора")
        return redirect('news:user', user_id)
    else:
        return redirect('news:error')


@permission_required('auth.add_group', login_url='news:error')
def add_moderator(request, user_id):
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=user_id)
        except:
            return redirect('news:error404')
        g = Group.objects.get(name="Модератор")
        g.user_set.add(user)
        messages.info(request, "Пользователю добавлены возможности модератора")
        return redirect('news:user', user_id)
    else:
        return redirect('news:error')


@permission_required('auth.delete_group', login_url='news:error')
def del_editor(request, user_id):
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=user_id)
        except:
            return redirect('news:error404')
        g = Group.objects.get(name="Редактор")
        g.user_set.remove(user)
        messages.info(request, "Права редактора удалены")
        return redirect('news:user', user_id)
    else:
        return redirect('news:error')


@permission_required('auth.delete_group', login_url='news:error')
def del_moderator(request, user_id):
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=user_id)
        except:
            return redirect('news:error404')
        g = Group.objects.get(name="Модератор")
        g.user_set.remove(user)
        messages.info(request, "Права модератора удалены")
        return redirect('news:user', user_id)
    else:
        return redirect('news:error')


@permission_required('news.add_news', login_url='news:error')
def save_news(request):
    if request.method == "POST":
        add_news = AddNewsForm(request.POST, request.FILES)
        if add_news.is_valid():
            add_news = add_news.cleaned_data
            ns = News(title=add_news['title'], text=add_news['text'], author_id=request.user.id,
                      image=add_news['image'], prev_text=add_news['prev_text'])
            ns.save()
            messages.info(request, "Новость опубликована")
        else:
            print_messages(request, add_news)
    return redirect('news:add_news')


@permission_required('news.add_news', login_url='news:error')
def add_news(request):
    return render(request, 'addnews.html', {'add_news': AddNewsForm()})


class UserView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(id=kwargs['user_id'])
            except:
                messages.error(request, 'Такого пользователя нет')
                return redirect('news:index')
            group = user.groups.all()
            usr = editor = moderator = False
            for i in group:
                if i.name == 'Пользователь':
                    usr = True
                elif i.name == 'Редактор':
                    editor = True
                elif i.name == 'Модератор':
                    moderator = True
            return render(request, 'user.html',
                          {'usr': user, 'group': group, 'u': usr, 'editor': editor, 'moderator': moderator})
        else:
            return redirect('user:auth')


def error405(request):
    return render(request, '405.html')


def error404(request):
    return render(request, '404.html')
