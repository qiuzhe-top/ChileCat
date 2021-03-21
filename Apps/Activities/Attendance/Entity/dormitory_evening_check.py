import datetime
from Apps.Life.models import *
from Apps.Activity.models import PunishmentDetails
from Apps.Activity.utils.activity_operate import *
# from Apps.Activity.utils import activity_operate
from .ser import TaskRecordSerializer


class DormitoryCheckTaskRecord(object):
    """
        晚查寝对象
        主要由数据表中的：执行人，被执行人（被查学生），原因，分值，创建时间，最后修改时间，寝室 组成
    """

    @staticmethod
    def leaks_view(time=datetime.date.today()):
        print(time)
        ret = TaskRecord.objects.filter(created_time__date=time).extra(select={
            "created_time": "DATE_FORMAT(created_time, '%%Y-%%m-%%d %%H:%%i:%%s')",
            "last_modify_time": "DATE_FORMAT(last_modify_time, '%%Y-%%m-%%d %%H:%%i:%%s')",
        })
        return TaskRecordSerializer(instance=ret, many=True).data

    @staticmethod
    def create(data):
        """创建一张记录表,主要检查数据缺失"""
        task_type = Manage.objects.get(id=data['task_type'])
        room_str = str(Room.objects.get(id=data['room']))
        task_record = TaskRecord.objects.create(
            task_type=task_type,
            worker=User.objects.get(id=data['worker']),
            student_approved=User.objects.get(id=data['student_approved']),
            reason=PunishmentDetails.objects.get(id=data['reason']),
            room_str=room_str,
            last_modify_time=datetime.datetime.now(),
        )
        task_record.reason_str = task_record.reason.name
        task_record.save()
        print(task_record, "已创建")


class DormitoryEveningCheck(AttendanceOperateInterface):
    """
    晚查寝对象相关操作
    """

    def __init__(self, manage_id: int):
        super().__init__(manage_id)
        if self._activity.types != "dorm":
            raise DormitoryEveningCheckException("非晚查寝活动意外的调用了晚查寝活动")

    def initialization(self) -> bool:
        Room.objects.all().update(status="0")
        self._activity.console_code = "0"
        self._activity.save()
        print("Manage id 为", self._activity.id, "更新为0.\n活动初始化完成")
        return True

    def leak_submit(self, leak_data):
        if self._activity.console_code == "0":
            raise ActivityInitialization("活动未开始")
        DormitoryCheckTaskRecord.create(leak_data)

    def today_leaks(self, date=datetime.date.today()):
        return DormitoryCheckTaskRecord.leaks_view()

