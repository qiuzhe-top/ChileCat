'''
Author: 邹洋
Date: 2021-08-20 10:31:45
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-10 18:08:40
Description: 
'''

from Apps.User.models import Token
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import RequestsClient

User = get_user_model()


# Create your tests here.
class Task(TestCase):
    
    
    def test_api(self):
        print(000)
