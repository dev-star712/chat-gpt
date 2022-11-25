from django.contrib.auth.models import User 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 

from apps.chat.permissions import RoomPermission
from rest_framework import viewsets
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response

from chat_app.pagination import CustomPagination
from apps.chat.models import Room
from apps.chat.serializers import RoomSerializer
from . import serializers, forms
from rest_framework import serializers as rest_serializer
from rest_framework.views import APIView

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
    return render(request, 'public/my-room.html')

@api_view(['GET'])
@login_required
def delete_room_api(request, room_code):
    object = get_object_or_404(Room, room_code=room_code)
    if object.creator == request.user:
        object.delete()
        return Response({"success":True})
    return Response({"success":False}, 403)

@api_view(['GET'])
@login_required
def refresh_code_api(request, room_code):
    object = get_object_or_404(Room, room_code=room_code)
    if object.creator == request.user:
        object.save()
        return Response({"success":True, "room_code":object.room_code})
    return Response({"success":False})

@api_view(['GET'])
@login_required
def my_room_api(request):
    # https://stackoverflow.com/questions/34043378/how-to-paginate-response-from-function-based-view-of-django-rest-framework
    paginator = CustomPagination()
    paginator.page_size = 8
    queryset = Room.objects.filter(creator=request.user)
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = RoomSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@login_required
def room_settings(request, room_code):
    
    object = get_object_or_404(Room, room_code=room_code)

    if request.user != object.creator:
        return redirect('profile')

    serializer = RoomSerializer(instance=object)
    
    # manipulate data render 

    users = object.chat_set.all()

    if len(users) != 0:
        users_id = [a.get('from_user') for a in users.values('from_user') if a.get('from_user') != request.user.pk]
    else:
        users_id = [request.user.pk]
    
    child = User.objects.filter(pk__in=users_id) # change list to QuerySet
    child_field = rest_serializer.PrimaryKeyRelatedField(queryset=child)
    serializer.fields['blocked_users'] = rest_serializer.ManyRelatedField(child_relation=child_field)
    
    return render(request, 'public/room-settings.html', {'serializer':serializer,'pk':object.pk})

class RoomSettingApi(APIView):
    permission_classes = [RoomPermission]

    def post(self, request):
        object = self.get_object()
        serializer = RoomSerializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success":True})
    
    def get_object(self):
        pk = self.request.data.get('pk')
        object = get_object_or_404(Room, pk=pk)
        return object 
    
def login_view(request):
    serializer = serializers.LoginSerializer()
    return render(request, 'public/login.html', {'serializer':serializer})

def register_view(request):
    serializer = serializers.UserSerializer()
    return render(request, 'public/register.html',context={'serializer':serializer})

def index_page(request):
    return render(request, 'public/index.html')
