"""
导入urls
"""
from django.urls import path
from . import views

urlpatterns = [
    # 获取能开什么活动
    path('idcode', views.VerificationCode.as_view(), name='VerificationCode'),
    # 控制活动
    path('switchknowing', views.SwitchKnowing.as_view(), name='SwitchKnowing'),
    # 我的活动
    path('myactive', views.MyActive.as_view(), name='MyActive'),
]
