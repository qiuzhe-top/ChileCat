import json
from django.contrib.auth.models import User
from . import task
from .. import models,serializers
from Apps.SchoolInformation import models as SchoolInformationModels

'''
晚查寝
'''


def is_number(s):
    '''判断字符串是否为数字
    '''
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


    def task_create(self,ids):
        '''创建任务
        '''
        self.task.buildings.set(ids)
        return True

    def clear_task(self):
        '''清除任务状态
        清空房间记录信息
        清空学生记录信息
        '''
        models.RoomHistory.objects.filter(task=self.task).update(is_knowing = False)
        models.TaskFloorStudent.objects.filter(task=self.task).update(flg = True)
        return '执行成功'
    def add_admin(self):
        '''添加管理员
        '''

        pass

    def switch(self):
        '''任务开启
        '''

        pass

    def scheduling(self,roster):
        '''排班
        '''
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
        models.TaskPlayer.objects.filter(task=self.task,is_admin=False).delete()

        # 开始用户任务绑定
        for u in user_list:
            models.TaskPlayer.objects.get_or_create(task=self.task,user=u,is_admin=False)

        self.task.roster = json.dumps(roster)
        self.task.save()
        return '保存班表成功'

    def condition(self):
        '''查看考勤工作情况
        '''
        records = models.Record.objects.filter(task=self.task,manager=None)
        data = serializers.ConditionRecord(instance=records,many=True).data
        return data
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

    # def out_data(self):
    #     '''数据导出
    #     '''
    #     print("准备导出excel")
    #     response = HttpResponse(content_type='application/vnd.ms-excel')
    #     filename = datetime.date.today().strftime("%Y-%m-%d") + ' 学生缺勤表.xls'
    #     response['Content-Disposition'] = (
    #         'attachment; filename={}'.format(escape_uri_path(filename))
    #     )
    #     req_list = self.request.query_params
    #     time_get = req_list.get('date', -1)
    #     if time_get == -1:
    #         time_get = date.today()
    #     records = TaskRecord.objects.filter(Q(task_type="dorm") & Q(
    #         manager=None) & Q(created_time__date=time_get))
    #     if not records:
    #         return JsonResponse(
    #             {"state": "1", "msg": "当日无缺勤"}
    #         )
    #     ser_records = ser.TaskRecordExcelSerializer(
    #         instance=records, many=True).data
    #     if ser_records:
    #         ws = xlwt.Workbook(encoding='utf-8')
    #         w = ws.add_sheet('sheet1')
    #         w.write(0, 0, u'日期')
    #         w.write(0, 1, u'楼号')
    #         w.write(0, 2, u'班级')
    #         w.write(0, 3, u'学号')
    #         w.write(0, 4, u'姓名')
    #         w.write(0, 5, u'原因')
    #         row = 1
    #         for i in ser_records:
    #             k = dict(i)
    #             column = 0
    #             for j in k.values():
    #                 w.write(row, column, j)
    #                 column += 1
    #             row += 1
    #         # 循环完成
    #         # path = os.getcwd()
    #         # ws.save(path + "/leaksfile/{}".format(filename))
    #         output = BytesIO()
    #         ws.save(output)
    #         output.seek(0)
    #         response.write(output.getvalue())
    #         print("导出excel")

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

    def submit(self,data,room_id,worker_user):
        '''考勤提交
        '''
        if not self.task.is_open:
            return "活动未开始"

        # 获取房间对象
        room = SchoolInformationModels.Room.objects.get(id=room_id)

        # 添加房间检查记录
        obj,flg = models.RoomHistory.objects.get_or_create(room=room,task=self.task)
        obj.is_knowing = True
        obj.save()

        for d in data:
            # 获取用户
            user = User.objects.get(id = d['user_id'])

            task_floor_student,flg = models.TaskFloorStudent.objects.get_or_create(task=self.task,user=user)
            # 状态判断 1:撤销记录
            if d['status'] == '1':
                task_floor_student.flg = True
                task_floor_student.save()
                obj = {
                    'task':self.task,
                    'rule_str':'撤销查寝记录',
                    'room_str':room.name,
                    'grade_str':user.studentinfo.grade.name,
                    'student_approved':user,
                    'worker':worker_user,
                }
                models.Record.objects.create(**obj)
            elif d['status'] == '0':              
                
                reason = d['reason']
                rule_str = ''
                rule = None

                # 判断是否为规则ID
                if is_number(reason):
                    # 获取对应规则对象
                    rule = models.RuleDetails.objects.get(id=reason)
                    rule_str = rule.name
                else:
                    # 记录字符串函数
                    rule_str = reason

                obj = {
                    'task':self.task,
                    'rule_str':rule_str,
                    'room_str':room.name,
                    'grade_str':user.studentinfo.grade.name,
                    'student_approved':user,
                    'worker':worker_user,
                }

                if rule:
                    obj['rule'] = rule
                    obj['score'] = rule.score
                models.Record.objects.create(**obj)
                task_floor_student.flg = False
                task_floor_student.save()
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
        '''晚查寝-楼工作数据
        '''

        buildings = self.task.buildings.all()
        buildings_info = []
        for building in buildings:
            info = {"list": [], 'id': building.id,
                    'name': building.name + "号楼"}
            floors = building.floor.all()
            for floor in floors:
                floor = {'id': floor.id, 'name': "第" + floor.name + "层"}
                info['list'].append(floor)
            buildings_info.append(info)
        return buildings_info

    def room(self,floor_id):
        '''晚查寝-层工作数据
        '''
        d = {"0": "dorm_status", "1": "health_status"}
        if floor_id:
            rooms = models.Room.objects.filter(floor_id=floor_id).values(
                'id', 'name', 'health_status', 'dorm_status')
            for room in rooms:
                room['status'] = room[d[self.task.types]]
                del room['health_status']
                del room['dorm_status']
            return list(rooms)

    def room_students(self,room_id):
        '''晚查寝-房间工作数据
        '''
        room_info = []
        room = models.Room.objects.get(id=room_id)
        room_data = room.stu_in_room.all()
        for i in room_data:
            unit = {'id': i.student.id,
                    'name': i.student.userinfo.name, 'position': i.bed_position}
            obj,flg = models.TaskFloorStudent.objects.get_or_create(task=self.task,user = i.student)
            unit['status'] = obj.flg
            room_info.append(unit)
        return room_info

    # @staticmethod
    # def search_room(room_info):
    #     """xx#xxx解析"""
    #     building_name = room_info.strip().split("#")[0].strip()
    #     floor = room_info.strip().split("#")[1].strip()[0].strip()
    #     room = room_info.strip().split("#")[1].strip()[1:3].strip()
    #     building, flag = models.Building.objects.get_or_create(
    #         name=building_name)
    #     floor, flag = models.Floor.objects.get_or_create(
    #         building=building, name=floor)
    #     room, flag = models.Room.objects.get_or_create(name=room, floor=floor)
    #     return room

    # @staticmethod
    # def dormitory_exchange():
    #     # 待调换的数据
    #     """3#422"""
    #     data = {
    #         '20653w213': ['3', '4', '22'],
    #         '19530139': ['3', '3', '04'],
    #         '19530116': ['3', '3', '03'],
    #         '1853w115': ['3', '2', '14']
    #     }
    #     for item in data:
    #         try:
    #             user = models.User.objects.get(username=item)
    #             # 新寝室
    #             b = models.Building.objects.get(name=data[item][0])
    #             f = models.Floor.objects.get(name=data[item][1], building=b)
    #             r = models.Room.objects.get(name=data[item][2], floor=f)
    #             print('学生：', user, '旧寝室：',
    #                   user.stu_in_room.all()[0], '待换寝室：', r)
    #             models.StuInRoom.objects.filter(student=user).update(room=r)
    #         except:
    #             print('调换失败', item)
