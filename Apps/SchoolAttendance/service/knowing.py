from core.excel_utils import out_knowing_data
import datetime
import json
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from . import task
from .. import models, serializers
from Apps.SchoolInformation import models as SchoolInformationModels

'''
晚查寝
'''


def is_number(s):
    '''判断字符串是否为数字'''
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


class Knowing(object):
    def __init__(self, task_obj):
        if task_obj:
            self.task = task_obj
            self.user = self.task.user

    def task_create(self, ids):
        '''创建任务'''
        self.task.buildings.set(ids)
        return True

    def clear_task(self):
        '''清除任务状态
        清空房间记录信息
        清空学生记录信息
        '''

        return '执行成功'

    def add_admin(self):
        '''添加管理员'''

        pass

    def switch(self):
        '''任务开启'''

        pass

    def scheduling(self, roster):
        '''排班'''
        # 同类型的活动工作组
        user_list = []
        for item in roster:
            for layer in item['layer_list']:
                for user in layer['user']:
                    if len(item['title'][:1]) != 0 and len(user['username']) != 0:

                        # 当前工作用户   # TODO 如果用户查找失败怎么处理
                        u = User.objects.get(username=user['username'])
                        user_list.append(u)

        # 之前的班表记录清空
        models.TaskPlayer.objects.filter(task=self.task, is_admin=False).delete()

        # 开始用户任务绑定
        for u in user_list:
            models.TaskPlayer.objects.get_or_create(
                task=self.task, user=u, is_admin=False
            )

        self.task.roster = json.dumps(roster)
        self.task.save()
        return '保存班表成功'

    def condition(self):
        '''查看考勤工作情况'''

    # def progress(self):
    #     '''查看考勤进度
    #     '''
    #     pass

    # def undo_record(self):
    #     '''销假
    #     '''
    #     task_record = TaskRecord.objects.get(id=task_record_id)
    #     task_record.manager = manager
    #     task_record.save()
    #     print("晚查寝提交记录", task_record, "销假人添加:", manager)

    def out_data(self):
        '''数据导出'''
        pass

    # def get_task(self):
    #     '''执行人获取任务
    #     '''
    #     pass

    # def rule(self):
    #     '''获取规则
    #     '''
    #     pass

    # def student_information(self):
    #     '''获取学生信息
    #     '''
    #     pass

    def submit(self, data, worker_user):
        '''考勤提交'''
        if not self.task.is_open:
            return "活动未开始"
        room_id = data['room_id']

        # 获取房间对象
        room = SchoolInformationModels.Room.objects.get(id=room_id)

        # 添加房间检查记录
        obj, flg = models.RoomHistory.objects.get_or_create(room=room, task=self.task)
        obj.is_knowing = True
        obj.room.dorm_status = True
        obj.room.save()
        obj.save()

        rule_obj = models.Rule.objects.get(codename='0#001')
        rule_obj, f = models.RuleDetails.objects.get_or_create(
            name='查寝自定义', defaults={'rule': rule_obj, 'score': 1}
        )

        for d in data['user_list']:
            # 获取用户
            user = User.objects.get(id=d['user_id'])

            task_floor_student, flg = models.TaskFloorStudent.objects.get_or_create(
                task=self.task, user=user
            )
            # 状态判断 1:撤销记录
            if d['status'] == '1':
                task_floor_student.flg = True
                task_floor_student.save()
                t = datetime.datetime.now()
                models.Record.objects.filter(
                    star_time__date=t, worker=worker_user, student_approved=user
                ).update(manager=worker_user, rule_str='查寝：误操作撤销')

            elif d['status'] == '0':

                reason = d['reason']
                rule_str = ''
                rule = None

                # 判断是否为规则ID
                if is_number(reason):
                    # 获取对应规则对象
                    try:
                        rule = models.RuleDetails.objects.get(id=reason)
                        rule_str = rule.name
                    except:
                        rule = rule_obj
                        rule_str = reason
                else:
                    # 记录字符串函数
                    rule = rule_obj
                    rule_str = reason

                obj = {
                    'task': self.task,
                    'rule_str': rule_str,
                    'room_str': room.get_room(),
                    'grade_str': user.studentinfo.grade.name,
                    'student_approved': user,
                    'worker': worker_user,
                    'score': 1,  # 默认夜不归扣一分
                }

                if rule:
                    obj['rule'] = rule
                    obj['score'] = rule.score
                models.Record.objects.create(**obj)
                task_floor_student.flg = False
                task_floor_student.save()
                room.dorm_status = True
                room.save()
                # 写入历史记录
        return '执行成功'
        # act_id = Manage.objects.get(id=leak_data['act_id'])
        # room = Room.objects.get(id=leak_data['room_id'])
        # worker = leak_data['worker']
        # worker = User.objects.get(username="19530226")
        # leak_info_list = leak_data['leak_info_list']
        # for leak_info in leak_info_list:
        #     stu_approved = User.objects.get(id=leak_info['student_id'])
        #     history_record = TaskRecord.objects.filter(
        #         task_type=act_id,
        #         created_time__date=datetime.date.today(),
        #         student_approved=stu_approved
        #     ).order_by('-created_time')
        #     if history_record.exists():
        #         print("更新")
        #         if leak_info['status'] == "1":
        #             print("误操作销假")
        #             leak_info.pop('reason')
        #             leak_info['reason_str'] = "误操作"
        #             leak_info['manager'] = worker
        #         else:
        #             # status = 0,表示还是不在寝室，注意是“还是”，此时需要把manager去掉，辣鸡zy，把flag砍了4，只能从manager去判断销假
        #             print("记录继续更新为缺勤")
        #             leak_info['manager'] = None
        #             leak_info['reason'] = PunishmentDetails.objects.get(
        #                 id=leak_info['reason'])
        #         TaskRecordAntiSerializer().update(history_record.first(), leak_info)
        #     else:
        #         print("正常创建")
        #         reason = PunishmentDetails.objects.get(id=leak_info['reason'])
        #         if leak_info['status'] == "0":
        #             DormitoryCheckTaskRecord.create(
        #                 act_id,
        #                 worker,
        #                 stu_approved,
        #                 reason,
        #                 str(room)
        #             )
        #         # status=1代表在寝，不需要创建
        # RoomHistory.objects.create(room=room, manager=worker)

    # def executor_finish(self):
    #     '''执行人确认任务完成'''
    #     pass

    def storey(self):
        '''晚查寝-楼工作数据'''

        buildings = self.task.buildings.all()
        buildings_info = []
        for building in buildings:
            info = {"list": [], 'id': building.id, 'name': building.name + "号楼"}
            floors = building.floor.all()
            for floor in floors:
                floor = {'id': floor.id, 'name': "第" + floor.name + "层"}
                info['list'].append(floor)
            buildings_info.append(info)
        return buildings_info

    def room(self, floor_id):
        '''晚查寝-层工作数据'''
        d = {"0": "dorm_status", "1": "health_status"}
        if floor_id:
            rooms = models.Room.objects.filter(floor_id=floor_id).values(
                'id', 'name', 'health_status', 'dorm_status'
            )
            for room in rooms:
                room['status'] = room[d[self.task.types]]
                del room['health_status']
                del room['dorm_status']
            return list(rooms)

    def room_students(self, room_id):
        '''晚查寝-房间工作数据'''
        room_info = []
        room = models.Room.objects.get(id=room_id)
        room_data = room.stu_in_room.all()
        for i in room_data:
            unit = {
                'id': i.user.id,
                'name': i.user.userinfo.name,
                'position': i.bed_position,
            }
            obj, flg = models.TaskFloorStudent.objects.get_or_create(
                task=self.task, user=i.user
            )
            unit['status'] = obj.flg
            room_info.append(unit)
        return room_info
