from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

import public.views

urlpatterns = [
    path('', public.views.index_page),
    path('login', public.views.login_view, name='login'),
    path('register', public.views.register_view, name='register'),
    path('chat/', include('chat.urls'), name='chat'),
    path('api/user/', include('public.api_urls')),
    path('api/chat/', include('chat.api_urls')),
    path('admin/', admin.site.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
