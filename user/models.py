from django.db import models
from django.db.models.signals import pre_delete
from datetime import datetime
from django.conf import settings
from datetime import date
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse


# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    location = models.CharField(max_length=30,blank=True)
    friends_count = models.PositiveIntegerField(default=0)
    profile_pic = models.FileField(upload_to='profile_pics/',blank=True,null=True)

    def natural_key(self):
        return (self.user.username,)





class MediaDB(models.Model):
    """""All User Feed Items"""
    username = models.ForeignKey(User,on_delete=models.CASCADE,)
    m_url = models.FileField(blank=True,null=True)
    timeStamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    location = models.CharField(max_length=30)
    likes_count = models.BigIntegerField(default=0)

    class Meta:
        ordering = ["-timeStamp"]
        verbose_name_plural="Media DB"

    def __str__(self):
        """""Return model as a String"""
        return str(self.id)



class Friends(models.Model):
    """"Model for saving relationship of user and friends"""
    request_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='current_user')
    friend_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_friend')
    created_on = models.DateTimeField(auto_now_add=True,auto_now=False)

    class Meta:
        verbose_name_plural = "Friends"

    def __str__(self):
        return str(self.friend_id)



class Request(models.Model):
    """"Model for storing requests sent by user"""
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='befriend_user')
    requested_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='request_user')
    sent_on = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return str(self.requested_id)

class Likes(models.Model):
    """"Model for storing likes by user for media"""
    media_id = models.ForeignKey(MediaDB,on_delete=models.CASCADE)
    user_like_id = models.ForeignKey(User,on_delete=models.CASCADE)
    liked_on = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return str(self.user_like_id)

    class Meta:
        verbose_name_plural = "Likes"
        unique_together = (("media_id","user_like_id"),)
