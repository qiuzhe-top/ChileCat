'''
Author: 邹洋
Date: 2022-01-25 19:13:47
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-11 14:20:57
Description: 
'''
from django.conf.urls import url, re_path
from . import consumers
websocket_urlpatterns = [
    url(r'^ws/room/status$', consumers.RoomStatus.as_asgi()),
    # re_path(r'ws/game/controller/(?P<room_id>\w+)/(?P<user_id>\d+)$', consumers.GameController),
]

