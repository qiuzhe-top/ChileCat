"""查寝统一管理"""
from Apps.Life import models
from .exceptions import *


class Room(object):

    @staticmethod
    def building_info():
        """获取全部楼号"""
        buildings = models.Building.objects.all()
        buildings_info = []
        for building in buildings:
            info = {"list": [], 'id': building.id, 'name': building.name + "号楼"}
            floors = building.floor.all()
            for floor in floors:
                floor = {'id': floor.id, 'name': "第" + floor.name + "层"}
                info['list'].append(floor)
            buildings_info.append(info)
        return buildings_info

    @staticmethod
    def room_info(floor_id):
        """获取房间信息"""
        if floor_id:
            rooms = models.Room.objects.filter(floor_id=floor_id)
            room_list = []
            for i in rooms:
                room_list.append({'id': i.id, 'name': i.name,
                                  'status': i.status})
            return room_list
        raise RoomParamException("缺少参数(层号+楼号)")

    @staticmethod
    def student_info(room_id):
        """获取学生位置等信息"""
        room_info = []
        room = models.Room.objects.get(id=room_id)
        room_data = room.stu_in_room.all()
        for i in room_data:
            unit = {'id': i.student.id,
                    'name': i.student.userinfo.name, 'status': i.status, 'position': i.bed_position}
            room_info.append(unit)
        return room_info
