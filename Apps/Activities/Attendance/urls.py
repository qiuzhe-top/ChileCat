"""
导入urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('studentleak', views.StudentLeak.as_view(), name='StudentLeak'),
    path('recordsearch', views.RecordSearch.as_view(), name='RecordSearch'),
    path('exportexcel', views.ExportExcel.as_view(), name='ExportExcel'),
]
