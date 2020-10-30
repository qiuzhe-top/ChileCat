from django.urls import path
from . import views 

urlpatterns = [
    path('leave_type', views.LeaveType.as_view()),
    path('draft', views.Draft.as_view()),
    # path('drafts', views.Drafts.as_view()), #规划时写错了 具体为draft Put请求
    path('audit', views.Audit.as_view()),
]
