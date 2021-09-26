'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-23 19:22:12
Description: 
'''
from django.contrib import auth
from Apps.User.models import Token
from Apps.SchoolInformation.models import *
from cool.views import ErrorCode
from django.contrib.auth import authenticate, login

from django.test import Client, TestCase
import requests
from .views import Login
from rest_framework.test import APITransactionTestCase, RequestsClient
from django.contrib.auth import get_user_model
User = get_user_model()

class AuthTest(TestCase):
    # 用户测试类
    def setUp(self):
        self.name = '张三'
        self.username = '195101'
        self.password = '123456'
        self.password_repaet = self.password
        # self.grade_id = 1
        self.room_id = 1
        self.api = '/api/user/'
        self.http_api = 'http://127.0.0.1:8000' + self.api
        # 创建ID为1的班级
        # 创建ID为1的房间
        u = User.objects.create_user(username=self.username)
        u.set_password(self.password)
        u.save()
        self.client = RequestsClient()
        self.set_token()



    def get_reg_data(self):
        data = {}
        data['name'] = self.name
        data['password_repaet'] = self.password_repaet
        data['password'] = self.password
        data['username'] = self.username
        return data

    def get_user(self):
        return User.objects.get(username=self.username)

    def test_login(self):
        print('登录：成功登录')
        data = {}
        data['username'] = self.username
        data['password'] = self.password
        response = Client().post(self.api + 'login', data).json()
        print(response)
        self.assertEqual(response['code'], 0)

    def test_get_infomation(self):
        print('用户信息：获取用户信息')
        response = self.client.post(self.http_api+'information').json()
        print(response)
        self.assertEqual(response['code'], 0)

    def set_token(self):
        user = self.get_user()
        token = 'alsdjooyzxkhalsdjooyzxkhalsdjooyzxkhalsdjooyzxkh'
        Token.objects.get_or_create(user=user, defaults={'token': token})
        self.client.headers.update({'TOKEN': token})

    def test_register(self):
        print('注册:成功注册')
        data = self.get_reg_data()
        data['username'] += '10'
        response = Client().post(self.api + 'register', data).json()
        print(response)
        self.assertEqual(response['code'], 0)

    def test_register_error_duplicate_username(self):
        print('注册: 账号重复')
        data = self.get_reg_data()
        response = Client().post(self.api + 'register', data).json()
        print(response)
        self.assertEqual(response['code'], 5003)

    def test_register_error_different_password(self):
        print('注册: 两次密码不一致')
        data = self.get_reg_data()
        data['password_repaet'] += 'a'
        response = Client().post(self.api + 'register', data).json()
        print(response)
        self.assertEqual(response['code'], 5002)

    def test_edit_password(self):
        print('修改密码：正常修改')
        d =self.get_reg_data()
        data = {}
        data['password_old'] = d['password']
        data['password_new'] = d['password'] + 'a'
        data['password_new_repaet'] = data['password_new']
        response = self.client.post(self.http_api+'edit/password',data).json()
        user = authenticate(username=self.username, password=data['password_new'])
        print(response)
        self.assertIsNotNone(user)

    def test_edit_password_old(self):
        print('修改密码：原密码不对')
        d =self.get_reg_data()
        data = {}
        data['password_old'] = d['password'] + '4'
        data['password_new'] = d['password'] + 'a'
        data['password_new_repaet'] = data['password_new']
        response = self.client.post(self.http_api+'edit/password',data).json()
        print(response)
        self.assertEqual(response['code'],5007)