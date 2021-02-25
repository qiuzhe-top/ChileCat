"""活动控制"""
import math
import random
import datetime
from Apps.Life.models import Room, StuInRoom, Manage
from .exceptions import *


class ActivityControl(object):
    """活动控制"""

    def __init__(self):
        # TODO warning: if id=1 record is deleted system will destroyed.
        if Manage.objects.all().count() == 0:
            manage = Manage(1, datetime.date.today(), "000000", "0")
            manage.save()
        self.__flag = Manage.objects.get(id=1)

    def get_status(self):
        """获取活动状态"""
        return self.__flag.console_code

    def get_verification_code(self):
        """获取验证码"""
        return self.__flag.verification_code

    def generate_verification_code(self):
        """生成验证码"""
        today = datetime.date.today()
        verification_code = str(math.floor(1e5 * random.random()))
        if self.__flag.generate_time == today:
            self.__flag.verification_code = verification_code
        else:
            self.__flag.generate_time = today
            self.__flag.verification_code = verification_code
            self.__flag.console_code = "0"
        self.__flag.save()
        return self.__flag.verification_code, self.__flag.generate_time, self.__flag.console_code

    def switch(self):
        """开启/关闭活动"""
        self.__flag = "1" if self.__flag.console_code == "0" else "0"
        return self.__flag

    @staticmethod
    def initialization():
        """初始化活动"""
        rooms = Room.objects.all()
        for room in rooms:
            room.status = "0"
            room.save()
        status = StuInRoom.objects.all()
        for stu in status:
            stu.status = "0"
            stu.save()
        return True

    def verify(self, verification_code):
        """验证验证码"""
        if self.__flag.generate_time != datetime.date.today():
            return "今日未发布验证码"
        else:
            if self.__flag.verification_code == verification_code:
                return True
            else:
                return "验证码不通过"
