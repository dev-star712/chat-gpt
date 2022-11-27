from rest_framework import serializers
from rest_framework.utils import model_meta

from .models import Room, Chat

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room 
        fields = "__all__"
        lookup_field = "room_code"
        read_only_fields = ['room_code','creator']
        extra_kwargs = {k:{'required':False, 'allow_null':True, 'write_only':True} for k in ['active_bots','blocked_users']}
    
    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save(room_code=True)

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance
    
    def create(self, validated_data):
        room = Room(**validated_data)
        room.save(room_code=False)
        return room 
    
class ChatSerializer(serializers.ModelSerializer):
    from_user = serializers.CharField(source="from_user.username")

    class Meta:
        model = Chat 
        fields = '__all__'
        read_only_fields = ['room', 'from_user', 'text']

        extra_kwargs = {k: {'read_only':True} for k in read_only_fields}
