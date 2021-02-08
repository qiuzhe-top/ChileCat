'''
路由注册
'''
from django.urls import path
from . import views

urlpatterns = [
    path('info', views.Info.as_view(),name='Info'),
    path('newscat', views.NewsCat.as_view(),name='NewsCat')
    
]
