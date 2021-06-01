from django.urls import path
from . import views

# manage
urlpatterns = [
    path('test', views.Test.as_view()),
    path('api_per', views.ApiPer.as_view()),
    path('group_init', views.group_init),
    path('dormitory_exchange', views.dormitory_exchange),
    path('init_activity_permissions', views.init_activity_permissions),
    path('uinitialization_rules', views.uinitialization_rules),
    path('in_zaoqian_excel', views.in_zaoqian_excel.as_view()),
]
