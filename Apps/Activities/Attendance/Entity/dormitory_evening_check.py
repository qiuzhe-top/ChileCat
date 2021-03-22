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
    def create(act_id: Manage, worker: User, student_approved: User, reason: PunishmentDetails, room_str) -> TaskRecord:
        """创建可能不止一张记录表,主要检查数据缺失"""
        if act_id.types != "dorm":
            print("任务错误")
        task_record = TaskRecord.objects.create(
            task_type=act_id,
            worker=worker,
            student_approved=student_approved,
            reason=reason,
            reason_str=reason.name,
            room_str=room_str,
            last_modify_time=datetime.datetime.now(),
        )
        print(task_record, "已创建")
        return task_record


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
        """
            data:{
                "act_id":1,
                "room_id":1,
                "worker":User,(后台添加)
                "leak_info_list":[
                    {
                        "student_id":1,
                        "reason":1,(可以为空)
                        "status":"0"
                    },
                    {...}
                ]
            }
        """
        if self._activity.console_code == "0":
            raise ActivityInitialization("活动未开始")
        act_id = Manage.objects.get(id=leak_data['act_id'])
        room = Room.objects.get(id=leak_data['room_id'])
        worker = leak_data['worker']
        worker = User.objects.get(username="19530226")
        leak_info_list = leak_data['leak_info_list']
        for leak_info in leak_info_list:
            DormitoryCheckTaskRecord.create(
                act_id,
                worker,
                User.objects.get(id=leak_info['student_id']),
                leak_info['reason'],
                str(room)
            )
        # TODO 未完工
        for leak_info in leak_info_list:
            print(leak_info)
            student_approved = User.objects.get(id=leak_info['student_id'])
            history_record = TaskRecord.objects.filter(
                created_time__date=datetime.date.today(),
                student_approved=student_approved
            )
            # 如果被查过了
            leak_info['room'] = room
            leak_info['worker'] = worker
            if history_record.exists():
                history_record.delete()
                task_record = DormitoryCheckTaskRecord.create(

                )
                task_record.reason_str = "二次操作"
                task_record.last_modify_time = datetime.datetime.now()
                task_record.save()
            else:
                DormitoryCheckTaskRecord.create(

                )
                room.status = "1"
                room.save()
        RoomHistory.objects.create(room=room, manager=worker)

    def today_leaks(self, date=datetime.date.today()):
        return DormitoryCheckTaskRecord.leaks_view()
