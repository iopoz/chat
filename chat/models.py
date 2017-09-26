from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Subject(models.Model):
    subject_name = models.CharField(max_length=50)

    def __str__(self):
        return self.subject_name

    def __unicode__(self):
        return self.subject_name

class ChatRooms(models.Model):
    room_name = models.CharField(max_length=50)
    room_subject = models.ForeignKey(Subject)
    room_creator = models.ForeignKey(User)

    def __str__(self):
        return self.room_name

    def __unicode__(self):
        return self.room_name


class Chat(models.Model):
    message = models.CharField(max_length=140)
    msg_created = models.DateTimeField(auto_now_add=True)
    msg_author = models.ForeignKey(User)
    msg_room = models.ForeignKey(ChatRooms)

    def __unicode__(self):
        return self.message
