'''
Author: 邹洋
Date: 2021-05-19 23:35:55
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-08-27 13:26:52
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


from cool.views import get_api_doc_html,get_api_info
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.urls.conf import re_path
from django.views.static import serve

# drf_yasg2 从这里开始
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Tweet API",
#         default_version='v1',
#         description="Welcome to the world of Tweet",
#         terms_of_service="https://www.tweet.org",
#         contact=openapi.Contact(email="demo@tweet.org"),
#         license=openapi.License(name="Awesome IP"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

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
    path('api_doc.html', get_api_doc_html),
    # re_path(r'^doc(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0), name='schema-json'),  #<-- 这里
    # path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  #<-- 这里
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  #<-- 这里
]
# if settings.DEBUG:
#     urlpatterns.append(
#         path(
#             '%s/<path:path>' % settings.MEDIA_URL.strip('/'),
#             serve,
#             {'document_root': settings.MEDIA_ROOT},
#         )
#     )
