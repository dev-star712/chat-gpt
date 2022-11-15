from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from . import serializers
from .models import Room, Chat

class RoomViewSets(viewsets.ModelViewSet):
    
    serializer_class = serializers.RoomSerializer
    queryset = Room.objects.all()
    lookup_field = "room_code"
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        
        serializer.creator = self.request.user
        serializer.save()

        return serializer
    
    def retrieve(self, request, *args, **kwargs):
        lookup_field = self.lookup_field or self.lookup_url_kwarg
        queryset = Chat.objects.filter(room__room_code=self.kwargs[lookup_field])
        serializer = serializers.ChatSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
class ChatViewSets(viewsets.ModelViewSet):
    serializer_class = serializers.ChatSerializer
    queryset = Chat.objects.all()
        
def join_room(request, room_code):
    return render(request, 'chat/chat.html', context={'room_name':room_code})

def index_chat(request):
    return render(request, 'chat/index.html')
    