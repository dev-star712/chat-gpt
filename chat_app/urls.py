from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

import apps.public.views, apps.chat.views

urlpatterns = [
    path('', apps.public.views.index_page),
    path('profile', apps.public.views.profile, name='profile'),
    re_path(r'^login', apps.public.views.login_view, name='login'),
    path('register', apps.public.views.register_view, name='register'),
    path('profile/my-room', apps.public.views.my_room, name='my_room'),
    path('profile/room/<str:room_code>/setting', apps.public.views.room_settings, name='room_settings'),
    path('chat/', include('apps.chat.urls'), name='chat'),
    path('api/user/', include('apps.public.api_urls')),
    path('api/chat/', include('apps.chat.api_urls')),
    path('admin/', admin.site.urls)
] + static('static/', document_root=settings.STATIC_ROOT)