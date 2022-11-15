from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'public'

router = DefaultRouter()
router.register('', views.UserViewSets, basename='user')

urlpatterns = [
    path('register',views.register_api, name='api_register'),
    path('login', views.login_api)
]