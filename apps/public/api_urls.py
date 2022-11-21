from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'public'

urlpatterns = [
    path('register',views.register_api, name='api_register'),
    path('login', views.login_api),
    path('refresh-code/<str:room_code>', views.refresh_code_api, name='refresh_room_api'),
    path('getMe', views.getMe, name='get_me'),
    path('my-room', views.my_room_api, name='my_room'),
    path('delete-room/<str:room_code>',views.delete_room_api, name='delete_room_api'),
    path('profile', views.profile_api, name='profile_api'),
    path('change-password', views.change_password_api, name='change_password')
]