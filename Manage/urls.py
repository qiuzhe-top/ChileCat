from django.urls import path
from . import views


urlpatterns = [
    path('test', views.Test.as_view()),
    path('api_per', views.ApiPer.as_view()),
    path('group_init', views.group_init)
]
