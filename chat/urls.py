from django.urls import path

from . import views

urlpatterns = [
    path('room/<str:room_code>', views.join_room, name='join_room'),
    path('', views.index_chat, name='index_chat')
]
