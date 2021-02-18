'''
导入urls
'''
from django.urls import path
from . import views

urlpatterns = [
    path('leave_type', views.LeaveType.as_view(),name='LeaveType'),
    path('draft', views.Draft.as_view(),name='Draft'),
    path('audit', views.Audit.as_view(),name='Audit'),
    path('get_name', views.GetName.as_view(), name='GetName'),
]
