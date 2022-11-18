from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'public'

urlpatterns = [
    path('register',views.register_api, name='api_register'),
    path('login', views.login_api),
    path('getMe', views.getMe, name='get_me'),
    path('my-room', views.my_room, name='my_room'),
    path('profile', views.profile_api, name='profile_api'),
    path('change-password', views.change_password_api, name='change_password')
]