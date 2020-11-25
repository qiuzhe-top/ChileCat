from django.urls import path
from . import views

urlpatterns = [
    path('auth', views.Auth.as_view()), #Z-post
    path('information', views.Information.as_view()),
]
