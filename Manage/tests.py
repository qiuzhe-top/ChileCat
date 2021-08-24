'''
Author: 邹洋
Date: 2021-08-20 10:31:45
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-08-20 10:33:40
Description: 
'''

from Apps.User.models import Token
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import RequestsClient



# Create your tests here.
class Task(TestCase):
    
    
    def test_api(self):
        print(000)
