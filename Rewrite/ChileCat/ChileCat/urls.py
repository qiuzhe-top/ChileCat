'''
Author: 邹洋
Date: 2022-02-07 11:01:56
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 15:01:00
Description: 
'''
"""ChileCat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from cool.views import get_api_doc_html

apipatterns = [
    path('user/', include('AppUser.views')),
    path('school_information/', include('AppInformation.views.views')),
    path('school_attendance/', include('AppAttendance.views.views')),
]
urlpatterns = [
    path('cool/', include('cool.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(apipatterns)),
    path('doc', get_api_doc_html),
]