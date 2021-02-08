'''
导入urls
'''
from django.urls import path
from . import views

urlpatterns = [
    path('idcode', views.Idcode.as_view(),name='Idcode'),
    path('buildinginfo', views.Buildinginfo.as_view(),name='Buildinginfo'),
    path('roominfo', views.Roominfo.as_view(),name='Roominfo'),
    path('stupositioninfo', views.Stupositioninfo.as_view(),name='Stupositioninfo'),
    path('studentleak', views.Studentleak.as_view(),name='Studentleak'),
    path('recordsearch', views.Recordsearch.as_view(),name='Recordsearch'),
    path('switchknowing', views.SwitchKnowing.as_view(),name='SwitchKnowing'),
    path('exportexcel', views.ExportExcel.as_view(),name='ExportExcel'),
]
