'''
Author: 邹洋
Date: 2021-07-04 13:57:48
Email: 2810201146@qq.com
LastEditors: Please set LastEditors
LastEditTime: 2021-08-01 10:53:20
Description: 常用数据序列化
'''
from django.db import models

from Apps.SchoolInformation.models import Building,Floor,Room
def search_room(room_info):
    """3#106解析返回Room对象"""
    try:
        building_name = room_info.strip().split("#")[0].strip()
        floor = room_info.strip().split("#")[1].strip()[0].strip()
        room = room_info.strip().split("#")[1].strip()[1:3].strip()

        building, flag = Building.objects.get_or_create(name=building_name)
        floor, flag = Floor.objects.get_or_create(building=building, name=floor)
        room, flag = Room.objects.get_or_create(name=room, floor=floor)
        return room
    except Exception as e:
        print(e.args)
        return None

