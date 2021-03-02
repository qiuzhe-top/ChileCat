"""学生缺勤"""
import datetime
from Apps.Life.models import Manage, Room, StuInRoom, TaskRecord, User, RoomHistory
from Apps.Life.utils.exceptions import *
from Apps.Life.ser import TaskRecordAntiSerializer, TaskRecordSerializer


class Leak(object):
    """缺勤"""

    def __init__(self, request):
        if Manage.objects.get(id=1).generate_time != datetime.date.today():
            raise TimeActivityException("活动未开启")
        self.__request = request

    @staticmethod
    def today_leaks(date=datetime.date.today()):
        """缺勤查询"""
        if not date:
            date = datetime.date.today()
        data = TaskRecord.objects.filter(flag="0", created_time__date=date)

        return TaskRecordSerializer(instance=data, many=True).data

    def cancel(self):
        """销假"""
        record_id = self.__request.data['record_id']  # 同理,不使用get
        record = TaskRecord.objects.get(id=record_id)
        record.flag = "1"
        record.manager = self.__request.user
        record.save()

    def submit(self):
        """缺勤提交"""
        worker = self.__request.user  # 查寝人
        params = self.__request.data
        if Manage.objects.get(id=1).console_code == "0":
            raise TimeActivityException("活动未开启")
        if params['code'] != Manage.objects.get(id=1).verification_code:
            raise VerificationCodeException("验证码身份过期")
        print("缺勤提交函数data:", params)
        student_leaks = params['data']
        room = Room.objects.get(id=int(params.get('roomid', 0)))  # 被查房间
        if student_leaks:  # 如果有缺勤
            for leak in student_leaks:
                leak_params = {}
                student = User.objects.get(id=leak['id'])  # 不使用get是因为这是必要数据,如果缺失直接抛出异常终止
                status = leak['status']
                stu = StuInRoom.objects.get(student=student)
                # 把学生在寝室的状态置为不在
                stu.status = status
                stu.save()
                # 如果这个人被查过了,那么覆盖
                TaskRecord.objects.filter(created_time__date=datetime.date.today(), student_approved=student).delete()
                # 利用反序列化创建一条记录
                leak_params['worker'] = worker
                leak_params['student_approved'] = student
                leak_params['reason'] = leak.get('reason', "")
                leak_params['flag'] = leak['status']
                leak_params['last_modify_time'] = datetime.datetime.now()
                leak_params['room'] = room
                TaskRecordAntiSerializer().create(leak_params)
        room.status = "1"  # 房间被查过
        room.save()
        RoomHistory.objects.create(room=room, manager=worker, created_time=datetime.datetime.now())  # 谁查了这个房间
