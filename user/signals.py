from django.contrib.auth.models import User
from .models import *
from django.dispatch import receiver
from django.db.models.signals import pre_delete,post_save,pre_save
from django.db.models import F

@receiver(pre_delete,sender=Request)
def create_friend(sender,instance,*args,**kwargs):
    req_user = instance.user_id
    req_friend = instance.requested_id
    Friends.objects.create(request_id=req_user,friend_id=req_friend)
    Friends.objects.create(request_id=req_friend,friend_id=req_user)


@receiver(post_save,sender=Likes)
def postlikes(sender,instance,created,**kwargs):
    if created:
        media = instance
        MediaDB.objects.filter(id = media.media_id.id).update(likes_count=F('likes_count') + 1)
        #liked_post =
        #liked_post.likes_count = F('likes_count') + 1
        #liked_post.save()
        #liked_post.update(likes_count=F('likes_count') + 1)


@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()

    #{//
    #This below save method causes Recursion Error
    #instance.save()
    #//}
@receiver(post_save,sender=Friends)
def update_friends_count(sender,instance,created,**kwargs):
    if created:
        user_profile,profile_created = Profile.objects.get_or_create(user = instance.request_id)
        user_profile.friends_count=F('friends_count')+1
        user_profile.save()


