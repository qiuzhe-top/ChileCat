"""
导入urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('myactive', views.VerificationCode.as_view(), name='MyActive'),
    path('switchknowing', views.SwitchKnowing.as_view(), name='SwitchKnowing'),
]
