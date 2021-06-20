from django.urls import path
from . import views
from Apps.Permission.utils import expand_permission as ApiPermission
# manage
urlpatterns = [
    # 系统数据初始化
    path('data_init', views.DataInit.as_view()),
    # path('dormitory_exchange', views.dormitory_exchange),
    path('init_activity_permissions', views.init_activity_permissions),
    path('uinitialization_rules', views.uinitialization_rules),
    # 系统API权限更新
    path('init_api_permissions', ApiPermission.init_api_permissions),
    # path('in_zaoqian_excel', views.In_zaoqian_excel.as_view()),
]
