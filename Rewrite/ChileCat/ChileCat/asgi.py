'''
Author: 邹洋
Date: 2022-02-07 11:01:56
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-11 14:19:02
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
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChileCat.settings')
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