'''
Author: 邹洋
Date: 2021-07-04 13:57:48
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-09 19:37:13
Description: 数据模型方法
'''
from django.db import models

from Apps.SchoolInformation.models import *
from Apps.SchoolAttendance.models import *

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
def create_custom_rule(codename,name,score=1):
        '''创建自定义规则'''
        rule_obj = Rule.objects.get(codename=codename)
        rule_obj, f = RuleDetails.objects.get_or_create(
            name=name, defaults={'rule': rule_obj, 'score': score}
        )
        
        return rule_obj

class TimeClass():
    star_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建日期')
    last_time = models.DateTimeField(auto_now=True, verbose_name=u'最后修改日期')
