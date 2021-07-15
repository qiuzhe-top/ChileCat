from django.contrib.auth.models import User
from rest_framework.test import RequestsClient

from Apps.User.models import Token
from django.test import TestCase
from . import models
# Create your tests here.
class Task(TestCase):
    # 考勤任务测试类
    def setUp(self) -> None:
        self.username = '195101'
     
        self.api = '/api/attendance/'
        self.http_api = 'http://127.0.0.1:8000' + self.api

        task = models.Task.objects.create(is_open = True, types = '0')
        u = User.objects.create_user(username=self.username)
        u.save()

        self.client = RequestsClient()
        self.set_token()

    def get_user(self):
        return User.objects.get(username=self.username)


    def set_token(self):
        user = self.get_user()
        token = 'alsdjooyzxkhalsdjooyzxkhalsdjooyzxkhalsdjooyzxkh'
        Token.objects.get_or_create(user=user, defaults={'token': token})
        self.client.headers.update({'TOKEN': token})

    def test_task_obtain(self):
        data = {'type1':'0'}
        response =self.client.post(self.http_api+'task/obtain',data).json()
        print(response)
        # self.assertEqual(response['code'],5007)