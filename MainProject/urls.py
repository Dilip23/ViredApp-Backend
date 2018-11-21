"""MainProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL t8ik
    o urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from user.user_api import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.views.static import serve



router = DefaultRouter()
router.register(r'profile',views.UserCreateAPIViewSet)
router.register(r'login',views.LoginAPIViewSet,base_name='login')
router.register(r'feed',views.UserFeedViewSet,base_name='feed')
router.register(r'friends',views.FriendsViewSet,base_name='friends')



urlpatterns = [
    path(r'admin/', admin.site.urls),
    url(r'^user/', include(("user.user_api.urls","user"),namespace="user-info")),
    url(r'^',include(router.urls)),
#    url(r'^logout/',views.LogoutAPIView.as_view(),name='user-logout'),
    url(r'^request/$',views.RequestCreateAPIView.as_view(),name='friend-request'),
    url(r'^add/(?P<requested_id>\d+)/$',views.RequestDestroyAPIView.as_view(),name='request-destroy'),
    url(r'^request-list/$',views.RequestListAPIView.as_view(),name='request-list'),
    url(r'^likes/$',views.LikesCreateAPIView.as_view(),name='likes'),
    url(r'^likedby/(?P<media_id>\d+)/$',views.LikesListAPIView.as_view(),name='liked'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/',include(debug_toolbar.urls)),
    ] + urlpatterns
