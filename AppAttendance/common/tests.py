'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 14:58:17
Description: 
'''
from AppUser.models import Token
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import RequestsClient

from AppAttendance import models

User = get_user_model()


# Create your tests here.
class Task(TestCase):
    # 考勤任务测试类
    def setUp(self) -> None:
        self.username = '195101'

        self.api = '/api/school/attendance/'
        self.http_api = 'http://127.0.0.1:8000' + self.api

        u = User.objects.create_user(username=self.username)

        u.save()
        task = models.Task.objects.create(is_open=True, types='0')
        task.admin.add(u)
        task.save()
        self.task_id = task.id
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
        data = {'type':'0'}
        response =self.client.post(self.http_api+'task/obtain',data).json()
        print('任务：获取任务',response)
        self.assertEqual(response['code'],0)

    def test_TaskSwitch(self):
        data = {'task_id':self.task_id}
        response =self.client.post(self.http_api+'task/switch',data).json()
        print('任务：开启/关闭任务',response,data)

    def test_Scheduling(self):
        data = {'task_id':self.task_id}
        response =self.client.post(self.http_api+'scheduling',data).json()
        print('任务：获取班表',response,data)
        self.assertEqual(response['code'],0)

