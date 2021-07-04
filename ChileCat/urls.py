'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors: OBKoro1
LastEditTime: 2021-07-04 13:45:01
Description: file information
'''

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
#     path('api/user/', include(('Apps.User.urls', 'Apps.User'), namespace='User')),
#     path('api/school_information/', include(('Apps.SchoolInformation.urls',
#          'Apps.SchoolInformation'), namespace='SchoolInformation')),
#     path('api/school_attendance/', include(('Apps.SchoolAttendance.urls',
#          'Apps.SchoolAttendance'), namespace='SchoolAttendance')),
#     path('api/manage/', include(('Manage.urls', 'Manage'), namespace='Manage')),
]
