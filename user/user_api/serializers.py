from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from user.models import (MediaDB,
                         Friends,
                         Request,
                         Likes,
                         Profile,
                         )
from datetime import datetime
User = get_user_model()


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """"A serializer for user data request"""
    location = serializers.CharField(source='profile.location')
    friends_count = serializers.IntegerField(source='profile.friends_count',read_only=True)
    profile_pic = serializers.FileField(source='profile.profile_pic',allow_empty_file=True,allow_null=True)


    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'email',
            'password',
            'location',
            'friends_count',
            'profile_pic',
            )
        extra_kwargs = {
            'password':{'write_only':True},
            'friends_count':{'read_only':True},
        }

    def create(self, validated_data):
        """"Create and return a new User"""


        user = User(
            email = validated_data['email'],
            username = validated_data['username']
        )

        user.set_password(validated_data['password'])

        user.save()

        return user


class UserFeedSerializer(serializers.ModelSerializer):
    """"A serializer for User Feed Items"""
    m_url = serializers.FileField(allow_empty_file=False,use_url=True)
    username = serializers.StringRelatedField(many=False,read_only=True)
    class Meta:
        model = MediaDB
        fields = ('id','username','m_url','timeStamp','location','likes_count',)
        extra_kwargs = {
            'username':{'read_only':True},
            'timeStamp':{'read_only':True},
            'likes_count':{'read_only':True},
        }

class RequestSerializer(serializers.ModelSerializer):
    """A serializer for handling friend requests"""
    user_id = serializers.StringRelatedField(many=False)

    class Meta:
        model = Request
        fields=('id','user_id','requested_id','sent_on',)
        extra_kwargs = {
            'sent_on':{'read_only':True},
            'id':{'read_only':True},
        }



class FriendsSerializer(serializers.ModelSerializer):
    """"Ä serializer for handling friend relations of users"""
    request_id = serializers.StringRelatedField(many=False,read_only=True)
    friend_id = serializers.StringRelatedField(many=False,read_only=True)
    class Meta:
        model = Friends
        fields=('id','request_id','friend_id','created_on',)
        read_only_fields = ('id','request_id','friend_id','created_on',)

class LikesCreateSerializer(serializers.ModelSerializer):
    """A serializer for creating and showing likes for posts"""

    user_like_id = serializers.StringRelatedField(many=False)
    #media_id = serializers.StringRelatedField(many=False)
    class Meta:
        model = Likes
        fields = ('id','user_like_id','media_id','liked_on')
        read_only_fields = ('id','liked_on')

    def create(self, validated_data):
        return Likes.objects.create(**validated_data)

class LikesListSerializer(serializers.ModelSerializer):
    """Serializer to handle list of users liked a post"""
    media_id = serializers.StringRelatedField(many=False)
    user_like_id = serializers.StringRelatedField(many=False)
    class Meta:
        model = Likes
        fields = '__all__'
        read_only_fields = ('id','media_id','user_liked_id','liked_on',)
