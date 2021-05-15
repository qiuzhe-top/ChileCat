from django.urls import path
from . import views

urlpatterns = [
    # 获取学生信息
    path('student_information', views.StudentInformation.as_view(),
         name='StudentInformation'),
    
]
