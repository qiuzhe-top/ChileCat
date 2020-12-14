from django.urls import path
from . import views

urlpatterns = [
    path('auth', views.Auth.as_view()),
    path('information', views.Information.as_view()),
    path('class', views.ClassList.as_view()),
    path('bindwx', views.Bindwx.as_view()),
]
