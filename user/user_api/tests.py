from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status


from user.user_api.views import *
from django.contrib.auth import get_user_model
from user.models import *
User = get_user_model()

class UserAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='test_user',email='test_user@test.com',password='password')
        user.save()

        feed = MediaDB.objects.create(username = user,location='South Georgia')


    def test_single_user(self):
        u_count = User.objects.count()
        self.assertEqual(u_count,1)

    def test_post(self):
        feed_count = MediaDB.objects.count()
        self.assertEqual(feed_count,1)

    def test_feed_list(self):
        data ={}
        url = "loclahost:8000/feed/<?P<pk>\d+>/"
        respone = self.client.get(url,data,format='json')
        self.assertEqual(respone.status_code,status.HTTP_200_OK)