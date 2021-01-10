'''
导入urls
'''
from django.urls import path
from . import views

urlpatterns = [
    path('idcode', views.Idcode.as_view()),
    path('buildinginfo', views.Buildinginfo.as_view()),
    path('roominfo', views.Roominfo.as_view()),
    path('stupositioninfo', views.Stupositioninfo.as_view()),
    path('studentleak', views.Studentleak.as_view()),
    path('recordsearch', views.Recordsearch.as_view()),
]
