"""
导入urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('idcode', views.VerificationCode.as_view(), name='VerificationCode'),
    path('switchknowing', views.SwitchKnowing.as_view(), name='SwitchKnowing'),
]
