'''
Author: 邹洋
Date: 2021-08-20 10:31:45
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-12-05 19:14:02
Description: 
'''

from Apps.User.models import Token
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import RequestsClient

User = get_user_model()


