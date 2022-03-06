'''
Author: 邹洋
Date: 2022-02-07 11:01:56
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-28 15:18:51
Description: 
'''
"""
ASGI config for ChileCat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChileCat.settings.dev')

django.setup()

# application = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from AppAttendance.websocket.routing import websocket_urlpatterns
 
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    )
})