from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.response import Response

from .permissions import RoomPermission
from . import serializers
from .models import Room, Chat

from public import serializers as public_serializer
from django.shortcuts import get_object_or_404

class RoomViewSets(viewsets.ModelViewSet):
    
    serializer_class = serializers.RoomSerializer
    queryset = Room.objects.all()
    lookup_field = "room_code"
    permission_classes = [RoomPermission]
    
    def perform_create(self, serializer):
        
        serializer.creator = self.request.user
        serializer.save()

        return serializer
    
    def create(self, request, *args, **kwargs):
        instance = super().create(request, *args, **kwargs)
        return Response(
            {
                "status":"success", 
                "room_code":instance.data.get('room_code')
            }
        )

    def retrieve(self, request, *args, **kwargs):
        lookup_field = self.lookup_field or self.lookup_url_kwarg

        lookup_kwargs = {lookup_field: self.kwargs[lookup_field]}

        _ = get_object_or_404(Room, **lookup_kwargs)

        queryset = Chat.objects.filter(room__room_code=self.kwargs[lookup_field])
        
        serializer = serializers.ChatSerializer(queryset, many=True)
        return Response(serializer.data)

def profile(request):
    serializer = public_serializer.UserSerializer
    return render(request, 'chat/profile.html', {'serializer':serializer})

def create_room(request):
    return render(request, 'chat/create-room.html')

class ChatViewSets(viewsets.ModelViewSet):
    serializer_class = serializers.ChatSerializer
    queryset = Chat.objects.all()
        
def join_room(request, room_code):
    is_exist = Room.objects.filter(room_code=room_code).first()
    if not is_exist:
        return redirect('chat:index_chat')
    return render(request, 'chat/chat.html', context={'room_name':room_code})

def index_chat(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', context={'rooms':rooms})
    