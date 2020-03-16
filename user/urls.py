from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('auth/', views.AuthView.as_view(), name='auth'),
    path('reg/', views.RegView.as_view(), name='reg'),
    path('logout/', views.log_out, name='logout'),
]