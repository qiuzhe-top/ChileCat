"""ChileCat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

urlpatterns = [
    # path('', Index.as_view()),
    path('admin/', admin.site.urls),
    path('api/user/', include(('Apps.User.urls', 'Apps.User'), namespace='User')),
    path('api/career/', include(('Apps.Career.urls', 'Apps.Career'), namespace='Career')),
    path('api/ask/', include(('Apps.Ask.urls', 'Apps.Ask'), namespace='Ask')),
    # path('api/life/', include(('Apps.Life.urls', 'Apps.Life'), namespace='Life')),
    path('api/school_information/', include(('Apps.SchoolInformation.urls',
         'Apps.SchoolInformation'), namespace='SchoolInformation')),
    path('api/school_attendance/', include(('Apps.SchoolAttendance.urls',
         'Apps.SchoolAttendance'), namespace='SchoolAttendance')),
    # path('api/activity/', include(('Apps.Activity.urls',
    #      'Apps.Activity'), namespace='Activity')),
    path('api/manage/', include(('Manage.urls', 'Manage'), namespace='Manage')),
]
