'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-07-04 23:37:36
Description: 
'''
from django.urls import path
from . import views


urlpatterns = [
    # path('auth', views.Auth.as_view(), name='Auth'),
    # path('information', views.Information.as_view(), name='Information'),
    path('class', views.ClassList.as_view(), name='ClassList'),
    # path('bindwx', views.BindVx.as_view(), name='BindVx'),
]


