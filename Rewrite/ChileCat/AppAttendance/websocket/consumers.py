'''
Author: 邹洋
Date: 2022-01-25 19:21:57
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-12 09:55:14
Description: 
参考
https://www.jianshu.com/p/0f75e2623418
'''
from time import sleep
from urllib import request
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

from AppAttendance.views.parent import DormCallCache
conn = DormCallCache()
ROOM_GROUP_NAME = "room"
class RoomStatus(WebsocketConsumer):

    def connect(self):
        self.room_group_name = ROOM_GROUP_NAME
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        request = json.loads(text_data)
        key = DormCallCache.get_type_by_dorm_key(request['type'])
        buildings = request['buildings']
        # 获取任务内房间状态
        rooms_cache = conn.cache.hgetall(key + DormCallCache.ROOM)
        # 获取任务内学生状态
        users_cache = conn.cache.hgetall(key + DormCallCache.USER)
        # 获取房间->学生集合
        room_users_cache = conn.cache.hgetall(DormCallCache.STUDENTS)
        # 更加任务房间整理对应学生状态
        # room_users = conn.get_room_stu()
        user_info = {}
        for floor in buildings:
            rooms = buildings[floor]
            for room in rooms:
                room_str = floor + room

                try:
                    users = json.loads(room_users_cache[room_str])
                except:
                    users = {}

                for user in users:

                    try:
                        rooms[room][user] = users_cache[user]
                    except:
                        rooms[room][user] = '2'
                        
                user_info[room_str] = users
                try:
                    rooms[room]['status'] = rooms_cache[room_str]
                except:
                    rooms[room]['status'] = '2'

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'all.status', # 这里的type 实际上就是 下面的chat_message自定义函数
                'data': {'buildings':buildings,'info':user_info}
            }
        )

    def all_status(self, event):
        self.send(text_data=json.dumps({
            'type': 'all_status',
            'data': event['data']
        }))

    def send_status(self, event):
        self.send(text_data=json.dumps({
            'type': 'send_status',
            'data': event['data']
        }))
