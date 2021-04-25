import datetime
from Apps.Activities.Attendance.Entity import dormitory_evening_check
from ..models import Manage

related = {
    'dorm': dormitory_evening_check.DormitoryEveningCheck
}


class ActivityFactory(object):
    def __init__(self, manage_id):
        print("尝试加载id为", manage_id, "的活动!")
        self._activity = Manage.objects.get(id=manage_id)

    def initialization(self):
        """初始化活动"""
        related[self._activity.types](self._activity.id).initialization()

    def leak_submit(self, leak_data):
        """缺勤提交"""
        related[self._activity.types](self._activity.id).leak_submit(leak_data)

    @staticmethod
    def today_leaks(time=datetime.date.today()):
        """缺勤查询(默认今天)"""
        return dormitory_evening_check.DormitoryCheckTaskRecord.leaks_view(pram_time=time)

    def cancel(self, task_record_id, manager):
        """销假"""
        related[self._activity.types](self._activity.id).cancel(task_record_id, manager)

    def get_status(self):
        """获取活动状态"""
        return related[self._activity.types](self._activity.id).activity.console_code

    def switch(self):
        return related[self._activity.types](self._activity.id).switch()

    def generate_verification_code(self):
        return related[self._activity.types](self._activity.id).generate_verification_code()[0]

    def verify(self, code):
        return related[self._activity.types](self._activity.id).verify(code)
