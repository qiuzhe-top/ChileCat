from django.urls import path
from . import views
# school_information
urlpatterns = [
    # 获取学生信息
    path('student_information', views.StudentInformation.as_view(),
         name='StudentInformation'),
    path('add_user',views.AddUser.as_view(),name='AddUser')
]
