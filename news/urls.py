from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "news"

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:news_id>', views.NewsDetailsView.as_view(), name='details'),
    path('<int:news_id>/del_comment/<int:comment_id>', views.del_comment, name='del_comment'),
    path('mute/<int:user_id>', views.mute, name='mute'),
    path('unmute/<int:user_id>', views.unmute, name='unmute'),
    path('page/<int:page_num>', views.page, name='page'),
    path('add_news/', views.add_news, name='add_news'),
    path('save_news/', views.save_news, name='save_news'),
    path('error/', views.error405, name='error'),
    path('error404/', views.error404, name='error404'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>', views.UserView.as_view(), name='user'),
    path('add_editor/<int:user_id>', views.add_editor, name='add_editor'),
    path('add_moderator/<int:user_id>', views.add_moderator, name='add_moderator'),
    path('del_editor/<int:user_id>', views.del_editor, name='del_editor'),
    path('del_moderator/<int:user_id>', views.del_moderator, name='del_moderator'),
    path('del_news/<int:news_id>', views.del_news, name='del_news'),
    path('hide_news/<int:news_id>', views.hide_news, name='hide_news'),
    path('edit_news/<int:news_id>', views.edit_news, name='edit_news'),
    path('change_avatar/', views.change_avatar, name='change_avatar'),
    path('change_password/', views.change_password, name='change_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
