"""寝室信息管理"""
from Apps.Life import models
from .exceptions import *
from django.db.models import Q
from ..ser import *

class Room(object):
    
    @staticmethod
    def building_info(request):
        """获取全部楼号"""


    @staticmethod
    def room_info(floor_id,types):
        """获取房间信息"""
        

    @staticmethod
    def student_info(room_id):
        """获取学生位置等信息"""


