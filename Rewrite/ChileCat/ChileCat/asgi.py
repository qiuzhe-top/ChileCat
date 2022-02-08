'''
Author: 邹洋
Date: 2022-02-07 11:01:56
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 19:56:53
Description: 
'''
"""
ASGI config for ChileCat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChileCat.settings')

# application = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from AppAttendance.websocket.routing import websocket_urlpatterns
 
application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    )
})