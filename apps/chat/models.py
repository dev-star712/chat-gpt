from django.db import models
from django.contrib.auth.models import User 
import random, string 
from django.conf import settings

class Room(models.Model):
    ROOM_VISIBILITY = (
        (0, 'only user that know room code can join'),
        (1, 'Anyone can join, room will shown in chat index')
    )

    room_code = models.CharField(max_length=8)
    room_name = models.CharField(max_length=255)
    is_public = models.IntegerField(choices=ROOM_VISIBILITY, default=1)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    blocked_users = models.ManyToManyField(User, related_name='blocked_users_set')

    def save(self, room_code=True, *args, **kwargs):
        if not room_code:
            self.room_code = self.__generate_code()
        super().save(*args, **kwargs)
    
    def __repr__(self):
        return self.room_name
    
    def __str__(self):
        return self.room_name

    def __generate_code(self):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(8))

class Visitor(models.Model):
    user_agent = models.TextField(null=True)
    ip_addr = models.GenericIPAddressField()

    def save(self, *args, **kwargs):
        if self.user_agent in settings.USER_AGENT_BLACKLIST:
            return None 
        return super().save(*args, **kwargs)

    def __repr__(self):
        return '<user_agent:{}'.format(self.user_agent)    

class Chat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __repr__(self):
        return '<from_user:{}'.format(self.from_user.username)
