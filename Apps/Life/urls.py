"""
导入urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('idcode', views.VerificationCode.as_view(), name='VerificationCode'),
    path('buildinginfo', views.BuildingInfo.as_view(), name='BuildingInfo'),
    path('roominfo', views.RoomInfo.as_view(), name='RoomInfo'),
    path('stupositioninfo', views.StudentPositionInfo.as_view(), name='StudentPositionInfo'),
    path('studentleak', views.StudentLeak.as_view(), name='StudentLeak'),
    path('recordsearch', views.RecordSearch.as_view(), name='RecordSearch'),
    path('switchknowing', views.SwitchKnowing.as_view(), name='SwitchKnowing'),
    path('exportexcel', views.ExportExcel.as_view(), name='ExportExcel'),
]
