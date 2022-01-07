'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-01-07 18:30:38
Description: file information
'''

from cool.views import get_api_doc_html
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

apipatterns = [
    path('user/', include('Apps.User.views')),
    path('school_information/', include('Apps.SchoolInformation.views')),
    path('school_attendance/', include('Apps.SchoolAttendance.views')),
    path('manage/', include('Manage.views')),
]
urlpatterns = [
    path('cool/', include('cool.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(apipatterns)),
    path('doc', get_api_doc_html),
]
# if settings.DEBUG:
#     urlpatterns.append(
#         path(
#             '%s/<path:path>' % settings.MEDIA_URL.strip('/'),
#             serve,
#             {'document_root': settings.MEDIA_ROOT},
#         )
#     )
