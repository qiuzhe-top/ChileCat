from django.urls import path
from . import views

urlpatterns = [
    path('auth', views.Auth.as_view(), name='Auth'),
    path('information', views.Information.as_view(), name='Information'),
    path('class', views.ClassList.as_view(), name='ClassList'),
    path('bindwx', views.Bindwx.as_view(), name='Bindwx'),
    path('mymood', views.MoodManage.as_view(), name='MoodManage'),
    # path('validationToken', views.ValidationToken.as_view()),
]
