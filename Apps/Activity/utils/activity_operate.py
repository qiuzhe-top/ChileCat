################################################################
#           继承图：
#                       活动控制
#                        |
#                        |----活动管理表的处理
#                        |
#                        |----具体活动控制的抽象接口->针对缺勤表的公共功能
#                                |
#                                |----不同子活动实现接口的功能
################################################################
import math
import random
import datetime
from Apps.Activity.models import Manage, User, TaskRecord
from Apps.Activity.utils.exceptions import *


# 以后可以把继承关系改成更基础的活动
class AttendanceActivityControl(object):
    """
        考勤活动控制
        由于每次活动类只控制一个活动，禁止在view的类初始化，请在get等方法使用
    """

    def __init__(self, manage_id: int):
        """初始化关于什么学院的什么活动"""
        self._activity = Manage.objects.get(id=manage_id)

    def get_total(self):
        """获取活动状态全部信息"""
        return self._activity

    def get_status(self):
        """获取活动状态"""
        return self._activity.console_code

    def generate_verification_code(self):
        """生成验证码"""
        today = datetime.date.today()
        Manage()
        verification_code = str(math.floor(1e5 * random.random()))
        flag = self._activity
        if flag.generate_time == today:
            flag.verification_code = verification_code
        else:
            flag.generate_time = today
            flag.verification_code = verification_code
            flag.console_code = "0"
        flag.save()
        return flag.verification_code, flag.generate_time, flag.console_code

    def get_verification_code(self):
        """获取验证码"""
        verification_code = {
            'generate_time': self._activity.generate_time,
            'verification_code': self._activity.verification_code
        }
        return verification_code

    def switch(self):
        """切换活动状态活动"""
        self._activity.console_code = "1" if self._activity.console_code == "0" else "0"
        self._activity.save()
        print("活动:", self._activity.code_name, "状态切换成功,当前状态为:", "未开启" if self._activity.console_code == "0" else "开启")
        return self._activity.console_code

    def verify(self, verification_code: str):
        """核对验证码"""
        if self._activity.verification_code == verification_code:
            return True
        return False

    @property
    def activity(self):
        return self._activity


class AttendanceOperateInterface(AttendanceActivityControl):
    """考勤活动操作的接口"""

    def initialization(self):
        """初始化活动"""
        raise ActivityException('没有指定活动对象')

    def construction(self):
        """开始活动"""
        raise ActivityException('没有指定活动对象')

    def leak_submit(self, leak_data):
        """缺勤提交"""
        raise ActivityException('没有指定活动对象')

    def today_leaks(self, date=datetime.date.today()):
        """缺勤查询(默认今天)"""
        raise ActivityException('没有指定活动对象')

    @staticmethod
    def cancel(task_record_id: int, manager: User):
        """销假"""
        task_record = TaskRecord.objects.get(id=task_record_id)
        task_record.manager = manager
        task_record.save()
        print("晚查寝提交记录", task_record, "销假人添加:", manager)

    def destruction(self):
        """结束活动"""
        raise ActivityException('没有指定活动对象')
