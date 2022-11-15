from django.contrib.auth.models import User 
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User 

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import serializers

class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    

@api_view(['POST'])
def login_api(request):
    serializer = serializers.LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = User.objects.get(username=serializer.validated_data)
        login(request, user)
        return Response({"success":True})
    else:
        print(serializer.errors)
    return Response({"success":False, "message":"Invalid username/password!"})

@api_view(['POST'])
def register_api(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True})
    else:
        return Response(serializer.errors)
    

def login_view(request):
    serializer = serializers.LoginSerializer()
    return render(request, 'public/login.html', {'serializer':serializer})

def register_view(request):
    serializer = serializers.UserSerializer()
    return render(request, 'public/register.html',context={'serializer':serializer})

def index_page(request):
    return render(request, 'public/index.html')
