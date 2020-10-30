from django.urls import path
from . import views 

urlpatterns = [
    path('leave_type', views.LeaveType.as_view()),
    path('draft', views.Draft.as_view()),
    path('drafts', views.Drafts.as_view()),
    path('audit', views.Audit.as_view()),
]
