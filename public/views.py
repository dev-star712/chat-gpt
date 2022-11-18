from django.contrib.auth.models import User 
from django.shortcuts import render
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 

from rest_framework import viewsets
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.pagination import CustomPagination
from chat.models import Room
from chat.serializers import RoomSerializer
from . import serializers, forms

class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer    
    
    def perform_update(self, serializer):
        print(serializer)
        return super().perform_update(serializer)

@login_required
@api_view(['POST'])
def profile_api(request):
    form = forms.ProfileForm(data=request.data, instance=request.user)
    if form.is_valid():

        return Response({"success":True})
    
    return Response(json.loads(form.errors.as_json()))

@login_required
@api_view(['POST'])
def change_password_api(request):
    form = forms.CustomChangePassword(request.user, request.data)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return Response({"success":True})
    return Response(json.loads(form.errors.as_json()))

@api_view(['POST'])
def login_api(request):
    serializer = serializers.LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = User.objects.get(username=serializer.validated_data)
        login(request, user)
        return Response({"success":True})

    return Response({"success":False, "message":"Invalid username/password!"})

@login_required
def profile(request):
    #serializer = serializers.UserSerializer()
    form = forms.ProfileForm(instance=request.user)
    password_form = forms.CustomChangePassword(request.user)
    return render(request, 'public/profile.html', {'form':form, 'password_form':password_form})

@api_view(['POST'])
def register_api(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True})
    else:
        return Response(serializer.errors)

@api_view(['GET'])
def getMe(request):
    ip_addr = request.META.get('HTTP_X_FORWADED_FOR') or request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')

    return Response(
        {
            'ip_address':ip_addr,
            'user_agent':user_agent
        }
    )

@api_view(['GET'])
@login_required
def my_room(request):
    # https://stackoverflow.com/questions/34043378/how-to-paginate-response-from-function-based-view-of-django-rest-framework
    paginator = CustomPagination()
    queryset = Room.objects.filter(creator=request.user)
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = RoomSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


def login_view(request):
    serializer = serializers.LoginSerializer()
    return render(request, 'public/login.html', {'serializer':serializer})

def register_view(request):
    serializer = serializers.UserSerializer()
    return render(request, 'public/register.html',context={'serializer':serializer})

def index_page(request):
    return render(request, 'public/index.html')
