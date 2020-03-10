from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "news"

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:news_id>', views.details, name='details'),
    path('<int:news_id>/del_comment/<int:comment_id>', views.del_comment, name='del_comment'),
    path('mute/<int:user_id>', views.mute, name='mute'),
    path('unmute/<int:user_id>', views.unmute, name='unmute'),
    path('page/<int:page_num>', views.page, name='page'),
    path('addnews/', views.addNews, name='addNews'),
    path('error/', views.error, name='error'),
    path('profile/', views.profile, name='profile'),
    path('user/<int:user_id>', views.user_profile, name='user'),
    path('add_editor/<int:user_id>', views.add_editor, name='add_editor'),
    path('add_moderator/<int:user_id>', views.add_moderator, name='add_moderator'),
    path('del_editor/<int:user_id>', views.del_editor, name='del_editor'),
    path('del_moderator/<int:user_id>', views.del_moderator, name='del_moderator'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
