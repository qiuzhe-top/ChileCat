"""活动控制"""
import math
import random
import datetime
from Apps.Life.models import Room, StuInRoom, Manage
from .exceptions import *


class ActivityControl(object):
    """活动控制"""

    if not Manage.objects.filter(id=1).exists():
        Manage(1, datetime.date.today(), "000000", "0")
    __flag = Manage.objects.get(id=1)

    def get_flag(self):
        print('get_flag')
        return Manage.objects.get(id=1)

    def get_status(self):
        """获取活动状态"""
        return Manage.objects.get(id=1).console_code

    def get_verification_code(self):
        """获取验证码"""
        today = datetime.date.today()
        if self.get_flag().generate_time == today:
            return self.get_flag().verification_code
        else:
            raise TimeVerificationCodeException("今日未发布验证码")

    def generate_verification_code(self):
        """生成验证码"""
        today = datetime.date.today()
        verification_code = str(math.floor(1e5 * random.random()))
        print("random:", verification_code)
        if self.get_flag().generate_time == today:
            self.get_flag().verification_code = verification_code
        else:
            self.get_flag().generate_time = today
            self.get_flag().verification_code = verification_code
            self.get_flag().console_code = "0"
        self.get_flag().save()
        return self.get_flag().verification_code, self.get_flag().generate_time, self.get_flag().console_code

    def switch(self):
        """开启/关闭活动"""
        self.get_flag().console_code = "1" if self.get_flag().console_code == "0" else "0"
        self.get_flag().save()
        return self.get_flag().console_code

    @staticmethod
    def initialization():
        """初始化活动"""
        Room.objects.all().update(status="0")
        StuInRoom.objects.all().update(status="1")
        Manage.objects.all().update(console_code="0")
        return True

    def verify(self, verification_code):
        """验证验证码"""
        if self.get_flag().generate_time != datetime.date.today():
            raise TimeVerificationCodeException("今日未发布验证码")
        else:
            if self.get_flag().verification_code == verification_code:
                return True
            else:
                raise VerifyVerificationCodeException("验证不通过")
