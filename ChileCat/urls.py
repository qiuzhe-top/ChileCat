'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-07-11 15:50:16
Description: file information
'''
# from django.contrib import admin
# from django.urls import include, path

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/user/', include(('Apps.User.urls', 'Apps.User'), namespace='User')),
#     path('api/school_information/', include(('Apps.SchoolInformation.urls',
#          'Apps.SchoolInformation'), namespace='SchoolInformation')),
#     path('api/school_attendance/', include(('Apps.SchoolAttendance.urls',
#          'Apps.SchoolAttendance'), namespace='SchoolAttendance')),
#     path('api/manage/', include(('Manage.urls', 'Manage'), namespace='Manage')),
# ]


from cool.views import get_api_doc_html
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

apipatterns = [
    path('user/', include('Apps.User.views')),
    path('school_information/', include('Apps.SchoolInformation.views')),
    path('school_attendance/', include('Apps.SchoolAttendance.views')),
]
urlpatterns = [
    path('cool/', include('cool.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(apipatterns)),
    path('api_doc.html', get_api_doc_html),
]
# if settings.DEBUG:
#     urlpatterns.append(
#         path(
#             '%s/<path:path>' % settings.MEDIA_URL.strip('/'),
#             serve,
#             {'document_root': settings.MEDIA_ROOT},
#         )
#     )
