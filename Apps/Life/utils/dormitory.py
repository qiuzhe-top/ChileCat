"""寝室信息管理"""
from Apps.Life import models
from .exceptions import *
from django.db.models import Q
from ..ser import *

class Room(object):

    @staticmethod
    def building_info(request):
        """获取全部楼号"""
        permissions = request.user.get_all_permissions()
        floor_list = []
        for permission in permissions:
            # 查寝 查卫生 一次性获取
            index = permission.find('floor')
            if index > 0:
                floor_list.append(permission[-1:])
        buildings = models.Building.objects.filter(name__in=floor_list)
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
    def room_info(floor_id,types):
        """获取房间信息"""
        d = {"floor-health":"health_status","floor-dorm":"dorm_status"}
        if floor_id:
            rooms = models.Room.objects.filter(floor_id=floor_id).values('id','name','health_status','dorm_status')
            for room in rooms:
                room['status'] = room[d[types]]
                del room['health_status']
                del room['dorm_status']
            return list(rooms)
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

    @staticmethod
    def search_room(room_info):
        """xx#xxx解析"""
        building_name = room_info.strip().split("#")[0].strip()
        floor = room_info.strip().split("#")[1].strip()[0].strip()
        room = room_info.strip().split("#")[1].strip()[1:3].strip()
        building, flag = models.Building.objects.get_or_create(name=building_name)
        floor, flag = models.Floor.objects.get_or_create(building=building, name=floor)
        room, flag = models.Room.objects.get_or_create(name=room, floor=floor)
        return room

    @staticmethod
    def dormitory_exchange():
        # 待调换的数据
        """3#422"""
        data = {
            '20653w213': ['3', '4', '22'],
            '19530139': ['3', '3', '04'],
            '19530116': ['3', '3', '03'],
            '1853w115': ['3', '2', '14']
        }
        for item in data:
            try:
                user = models.User.objects.get(username=item)
                # 新寝室
                b = models.Building.objects.get(name=data[item][0])
                f = models.Floor.objects.get(name=data[item][1], building=b)
                r = models.Room.objects.get(name=data[item][2], floor=f)
                print('学生：', user, '旧寝室：', user.stu_in_room.all()[0], '待换寝室：', r)
                models.StuInRoom.objects.filter(student=user).update(room=r)
            except:
                print('调换失败', item)
