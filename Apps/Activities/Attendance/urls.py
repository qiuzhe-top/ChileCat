"""
导入urls
"""
from django.urls import path
from . import views

urlpatterns = [
    # 学生晚查寝缺勤提交
    path('studentleak', views.StudentLeak.as_view(), name='StudentLeak'),
    # 记录查询返回所有缺勤记录
    path('recordsearch', views.RecordSearch.as_view(), name='RecordSearch'),
    # 导出excel
    path('exportexcel', views.ExportExcel.as_view(), name='ExportExcel'),
]
