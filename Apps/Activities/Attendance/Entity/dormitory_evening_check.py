import datetime
import time
from Apps.Life.models import *
from Apps.Activity.models import PunishmentDetails
from Apps.Activity.utils.activity_operate import *
from Apps.Activity.utils import exceptions
# from Apps.Activity.utils import activity_operate
from .ser import TaskRecordSerializer
from Apps.Activity.ser import TaskRecordAntiSerializer
from django.core import serializers


class DormitoryCheckTaskRecord(object):
    """
        晚查寝对象
        主要由数据表中的：执行人，被执行人（被查学生），原因，分值，创建时间，最后修改时间，寝室 组成
    """

    @staticmethod
    def leaks_view(pram_time=datetime.date.today()):
        print("时间为", pram_time, "的缺勤名单")
        # 当销假人为空的时候为未销假
        # 官方不推荐使用extra插入sql语句,并且extra未来会被官方移除
        # ret = TaskRecord.objects.prefetch_related(
        #     "worker__userinfo", "student_approved__userinfo", "manager__userinfo"
        # ).filter(created_time__date=pram_time, manager=None).extra(select={
        #     "created_time": "DATE_FORMAT(created_time, '%%Y-%%m-%%d %%H:%%i:%%s')",
        #     "last_modify_time": "DATE_FORMAT(last_modify_time, '%%Y-%%m-%%d %%H:%%i:%%s')",
        # })
        ret = TaskRecord.objects.prefetch_related(
            "worker__userinfo", "student_approved__userinfo", "manager__userinfo"
        ).filter(created_time__date=pram_time, manager=None)
        task = TaskRecordSerializer(instance=ret, many=True).data
        return task

    @staticmethod
    def create(act_id: Manage, worker: User, student_approved: User, reason: PunishmentDetails, room_str, grade_str) \
            -> TaskRecord:
        """创建可能不止一张记录表,主要检查数据缺失"""
        if act_id.types != "dorm":
            print("任务错误")
        score = reason.score
        task_record = TaskRecord.objects.create(
            task_type=act_id,
            worker=worker,
            student_approved=student_approved,
            reason=reason,
            score=score,
            reason_str=reason.name,
            room_str=room_str,
            grade_str=grade_str,
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
        worker = User.objects.get(id=leak_data['worker'])
        leak_info_list = leak_data['leak_info_list']
        for leak_info in leak_info_list:
            stu_approved = User.objects.get(id=leak_info['student_id'])
            # 如果学生不在这个房间，抛出异常
            if not StuInRoom.objects.filter(student=stu_approved, room=room).exists():
                raise exceptions.DormitoryEveningCheckException("寝室无此学生"+str(stu_approved))
            history_record = TaskRecord.objects.filter(
                task_type=act_id,
                created_time__date=datetime.date.today(),
                student_approved=stu_approved
            ).order_by('-created_time')
            if history_record.exists():
                print("查寝记录更新")
                if leak_info['status'] == "1":
                    StuInRoom.objects.filter(student=stu_approved).update(status="1")
                    print("查寝人销假")
                    leak_info.pop('reason')
                    leak_info['reason_str'] = "误操作"
                    leak_info['manager'] = worker
                else:
                    # status = 0,表示还是不在寝室，注意是“还是”，此时需要把manager去掉，辣鸡zy，把flag砍了，只能从manager去判断销假
                    print("记录改为缺勤")
                    leak_info['manager'] = None
                    leak_info['reason'] = PunishmentDetails.objects.get(id=leak_info['reason'])
                    # 学生是否在寝状态更新为0
                    StuInRoom.objects.filter(student=stu_approved).update(status="0")
                TaskRecordAntiSerializer().update(history_record.first(), leak_info)
            else:
                reason = PunishmentDetails.objects.get(id=leak_info['reason'])
                if leak_info['status'] == "0":
                    print("创建缺勤记录")
                    StuInRoom.objects.filter(student=stu_approved).update(status="0")
                    DormitoryCheckTaskRecord.create(
                        act_id,
                        worker,
                        stu_approved,
                        reason,
                        str(room),
                        stu_approved.studentinfo.grade.name
                    )
                # status=1代表在寝，不需要创建,当然status为1也有可能是误操作,但不会走到这里
        RoomHistory.objects.create(room=room, manager=worker)

    def today_leaks(self, date=datetime.date.today()):
        return DormitoryCheckTaskRecord.leaks_view()
