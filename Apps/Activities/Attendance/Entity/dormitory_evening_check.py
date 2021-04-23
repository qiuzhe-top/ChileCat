import datetime
from Apps.Life.models import *
from Apps.Activity.models import PunishmentDetails
from Apps.Activity.utils.activity_operate import *
# from Apps.Activity.utils import activity_operate
from .ser import TaskRecordSerializer
from Apps.Activity.ser import TaskRecordAntiSerializer


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
        score = reason.score
        task_record = TaskRecord.objects.create(
            task_type=act_id,
            worker=worker,
            student_approved=student_approved,
            reason=reason,
            score=score,
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
        '''还原寝室状态'''
        roster = json.loads(self._activity.roster)
        floor = []
        try:
            for item in roster:
                floor.append(int(item['title'][:1]))
            Room.objects.filter(floor__in=floor).update(status="0")
        except:
            print('初始化寝室失败 班表数据异常')

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
        if not self._activity.console_code:
            raise ActivityInitialization("活动未开始")
        act_id = Manage.objects.get(id=leak_data['act_id'])
        room = Room.objects.get(id=leak_data['room_id'])
        worker = leak_data['worker']
        worker = User.objects.get(username="19530226")
        leak_info_list = leak_data['leak_info_list']
        for leak_info in leak_info_list:
            stu_approved = User.objects.get(id=leak_info['student_id'])
            history_record = TaskRecord.objects.filter(
                task_type=act_id,
                created_time__date=datetime.date.today(),
                student_approved=stu_approved
            ).order_by('-created_time')
            if history_record.exists():
                print("更新")
                if leak_info['status'] == "1":
                    print("误操作销假")
                    leak_info.pop('reason')
                    leak_info['reason_str'] = "误操作"
                    leak_info['manager'] = worker
                else:
                    # status = 0,表示还是不在寝室，注意是“还是”，此时需要把manager去掉，辣鸡zy，把flag砍了4，只能从manager去判断销假
                    print("记录继续更新为缺勤")
                    leak_info['manager'] = None
                    leak_info['reason'] = PunishmentDetails.objects.get(id=leak_info['reason'])
                TaskRecordAntiSerializer().update(history_record.first(), leak_info)
            else:
                print("正常创建")
                reason = PunishmentDetails.objects.get(id=leak_info['reason'])
                if leak_info['status'] == "0":
                    DormitoryCheckTaskRecord.create(
                        act_id,
                        worker,
                        stu_approved,
                        reason,
                        str(room)
                    )
                # status=1代表在寝，不需要创建
        RoomHistory.objects.create(room=room, manager=worker)

    def today_leaks(self, date=datetime.date.today()):
        return DormitoryCheckTaskRecord.leaks_view()
    def switch(self):
        '''活动开关'''
        console_code = self._activity.console_code
        console_code=not console_code
        if console_code:
            self.initialization()
        self._activity.console_code = console_code
        self._activity.save()
        return console_code

    def save_roster(self,roster):
        '''保存班表'''

        # 同类型的活动工作组
        active_groups = []
        for item in Manage.objects.filter(types=self._activity.types).values_list('code_name',flat=True):
            active_groups.append('work_'+item)
        user_all = []
        for item in roster:
            user_list = []
            for layer in item['layer_list']:
                for user in layer['user']:
                    if len(item['title'][:1])!=0 and len(user['username'])!=0:
                        # 当前工作用户
                        u = User.objects.get(username=user['username'])
                        g = u.groups.filter(name__in=active_groups)
                        if g.exists():
                            print(g)
                            for group in g:
                                # 用户退出已经有的同类型不同分院的工作组
                                group.user_set.remove(u)
                        user_list.append(user['username'])
                        
            group_clean('dorm_'+item['title'][:1])
            group_add_user('dorm_'+item['title'][:1],user_list)
            user_all+=user_list
        print(user_all)
        # 添加对应工作组
        n = 'work_'+ self._activity.college.code_name + '_' + self._activity.types
        group_clean(n)
        group_add_user(n,user_all)
        self._activity.roster=json.dumps(roster)
        self._activity.save()
        return self._activity