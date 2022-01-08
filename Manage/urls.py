'''
Author: 邹洋
Date: 2021-12-01 08:08:08
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-01-08 19:23:15
Description: 
'''
from django.urls import path
from . import views
from core.rest_permission.init_api_url import init_api_permissions

# manage
urlpatterns = [
    # 系统数据初始化
    # path('data_init', views.DataInit.as_view()),
    # 系统API权限更新
    path('init_api_permissions', init_api_permissions),
    # path('in_zaoqian_excel', views.In_zaoqian_excel.as_view()),
]
