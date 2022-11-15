from django.db import models
from django.contrib.auth.models import User 

import random, string 

class Room(models.Model):
    room_code = models.CharField(max_length=8)
    room_name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def save(self, *args, **kwargs):
        self.room_code = self.__generate_code()
        super().save(*args, **kwargs)
    
    def __repr__(self):
        return self.room_name

    def __generate_code(self):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    

class Chat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    
    def __repr__(self):
        return '<from_user:{}'.format(self.from_user.username)
