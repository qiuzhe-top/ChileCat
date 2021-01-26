'''
路由注册
'''
from django.urls import path
from . import views

urlpatterns = [
    path('info', views.Info.as_view()),
    path('newscat', views.NewsCat.as_view())
    
]
