from rest_framework import generics,request,mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status,viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated



from user.models import (
    MediaDB,
    Friends,
    Profile,
    Likes,
    Request,
    )
from django.contrib.auth.models import User
from django.db.models import Q
from .serializers import \
    (UserProfileCreateSerializer,
     UserFeedSerializer,
     RequestSerializer,
     FriendsSerializer,
     LikesCreateSerializer,
     LikesListSerializer,
     )
from . import permissions


class UserCreateAPIViewSet(viewsets.ModelViewSet,mixins.UpdateModelMixin):
    """"A View which handles  Creating  and Updating User Profile"""
    serializer_class = UserProfileCreateSerializer
    queryset = User.objects.all()
    paginator = None
    #pagination_classes = None
    #paginate_by = None
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('username','email',)




class LoginAPIViewSet(viewsets.ViewSet):
    ''''Checks email and password and return an authToken'''
    serializer_class = AuthTokenSerializer

    def create(self,request):
        ''''Use the obtainAuthToken APIVIewto validate and create a Token .'''

        return ObtainAuthToken().post(request)
#
#
#Implement Logout Operation on Client Side
#
#
# class LogoutAPIView(APIView):
#     ''''View for handling User Logout Requests'''
#     def get(self,request,format=None):
#         request.user.authtoken.delete()
#         return Response(status=status.HTTP_200_OK)


class UserFeedViewSet(viewsets.ModelViewSet):
    """""Handles Creating ,Reading and updating profile Feed"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.PostOwnStatus,IsAuthenticated)
    pagination_class = LimitOffsetPagination
    serializer_class = UserFeedSerializer
    def get_queryset(self):
        return  MediaDB.objects.filter(username__user_friend__request_id=self.request.user)

    def perform_create(self, serializer):
        """""Sets the user Profile to logged in user"""

        serializer.save(username = self.request.user)

class RequestCreateAPIView(generics.CreateAPIView):
    """View for creating requests"""
    serializer_class = RequestSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=self.request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class RequestDestroyAPIView(generics.DestroyAPIView):
    """View for destroying requests"""
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = 'id'
    lookup_url_kwarg = 'requested_id'



class RequestListAPIView(generics.ListAPIView):
    """View for retrieving list of requests of user"""
    serializer_class = RequestSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = LimitOffsetPagination
    def get_queryset(self,*args,**kwargs):
        queryset_list = Request.objects.all().filter(requested_id=self.request.user)
        param = self.request.GET.get('q')
        if param:
            queryset_list = queryset_list.filter(user_id__iexact = param)
        return queryset_list



class FriendsViewSet(viewsets.ModelViewSet):
    """"A Viewset for listing user's friends"""
    serializer_class = FriendsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = LimitOffsetPagination
    def get_queryset(self):
        #friends = Friends.objects.filter(request_id = self.request.user)
        #Optimized query
        friends = Friends.objects.select_related('request_id__profile').filter(request_id=self.request.user)
        return friends

class LikesCreateAPIView(generics.CreateAPIView):
    """"A viewset for creating and showing likes by post"""
    serializer_class = LikesCreateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Likes.objects.all()

    def post(self, request, *args, **kwargs):
        """Method for creating likes for Media per User"""
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_like_id=self.request.user)
        return  Response(serializer.data,status=status.HTTP_201_CREATED)

class LikesListAPIView(generics.ListAPIView):
    """View for retrieve list of users liked a post"""
    serializer_class = LikesListSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        m_id = self.kwargs['media_id']
        #users = Likes.objects.filter(media_id = m_id)
        #Optimized query
        users = Likes.objects.select_related('media_id__username').filter(media_id_id=m_id)
        return users
