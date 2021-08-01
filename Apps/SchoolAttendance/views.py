'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors: Please set LastEditors
LastEditTime: 2021-08-01 21:41:45
Description: 
'''
from copy import error
from core.common import is_number
from Apps.User.utils.auth import get_token_by_user
import datetime

from Apps.SchoolAttendance.pagination import RecordQueryrPagination
from Apps.SchoolInformation import models as SchoolInformationModels
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, ViewSite
from core.excel_utils import at_all_out_xls, excel_to_list, out_knowing_data
from core.query_methods import Concat
from core.views import *
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.aggregates import Sum
from django.db.models.query_utils import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from openpyxl.reader.excel import load_workbook
from rest_framework import fields

from . import models, serializers


site = ViewSite(name='SchoolInformation', app_name='SchoolInformation')

@site
class TaskObtain(Permission):

    name = _('获取任务')
    response_info_serializer_class = serializers.TaskObtain

    def get_context(self, request, *args, **kwargs):
        task = models.Task.objects.filter(admin=request.user,types=request.params.type)
        return serializers.TaskObtain(task,many=True, request=request).data
    class Meta:
        param_fields = (
            ('type', fields.CharField(label=_('任务类型'), max_length=1,help_text=' 0晚查寝 1查卫生 2晚自修')),
        )


@site
class TaskSwitch(TaskBase):
    
    name = _('开启/关闭任务')
    response_info_serializer_class = serializers.TaskSwitch

    def get_context(self, request, *args, **kwargs):
        task =self.get_task_by_user()
        task.is_open = not task.is_open
        task.save()
        return serializers.TaskSwitch(task,request=request).data

@site
class TaskRestKnowing(TaskBase):
    name = _('重置查寝任务状态')

    def get_context(self, request, *args, **kwargs):
        task = self.get_task_by_user()
        # TODO 请简化循环
        b = task.buildings.all()
        for i in b:
            for j in i.floor.all():
                for k in j.room.all():
                    k.dorm_status = False
                    k.save()

        models.RoomHistory.objects.filter(task=task).update(is_knowing=False)
        models.TaskFloorStudent.objects.filter(task=task).update(flg=True)


@site
class TaskRestLate(TaskBase):
    name = _('重置晚自修任务状态')

    def get_context(self, request, *args, **kwargs):
        task = self.get_task_by_user()
        models.UserCall.objects.filter(task=task).update(flg=None)



@site
class Scheduling(TaskBase):
    name = _('获取排版表')

    def get_context(self, request, *args, **kwargs):
        return json.loads(self.get_task_by_user().roster)


@site
class SchedulingUpdateKnowing(TaskBase):
    name = _('修改查寝班表')

    def get_context(self, request, *args, **kwargs):
        roster = request.params.roster
        user_list = []
        error = 0
        for item in roster:
            for layer in item['layer_list']:
                for user in layer['user']:
                    if len(item['title'][:1]) != 0 and len(user['username']) != 0:
                        try:
                            u = User.objects.get(username=user['username'])
                            user_list.append(u)
                        except:
                            error+=1

        self.init_scheduling(user_list,roster)
        if error != 0:
            return str(error) + '个学生排班失败'

    class Meta:
        param_fields = (
            ('roster', fields.JSONField(label=_('班表'))),
        )


@site
class SchedulingUpdateLate(TaskBase):
    name = _('修改晚自修班表')

    def get_context(self, request, *args, **kwargs):
        roster = request.params.roster
        user_list = []
        roster_new = []
        for item in roster:
            u = User.objects.filter(username=item['username'])
            if len(u) == 1:
                user_list.append(u[0])
                roster_new.append(item)

        self.init_scheduling(user_list,roster_new)
        return '执行成功' + '更新' + str(len(roster_new)) + '个学生' 
    class Meta:
        param_fields = (
            ('roster', fields.JSONField(label=_('班表'))),
        )

@site
class Condition(TaskBase):

    name = _('考勤学生记录情况')
    response_info_serializer_class = serializers.ConditionRecord

    def get_context(self, request, *args, **kwargs):
        task = self.get_task_by_user()
        now = datetime.datetime.now() 
        records = models.Record.objects.filter(
            task=task,
            manager=None,
            star_time__date=datetime.date(now.year, now.month, now.day),
        )
        return serializers.ConditionRecord(records, request=request,many=True).data
        

@site
class UndoRecord(TaskBase):
    name = _('销假(当前任务管理员)')

    def get_context(self, request, *args, **kwargs):
        task = self.get_task_by_user()
        record = models.Record.objects.get(task=task,id=request.params.record_id)
        record.manager=request.user
        record.save()

    class Meta:
        param_fields = (
            ('record_id', fields.CharField(label=_('考勤记录ID'), max_length=8)),
        )

@site
class UndoRecordAdmin(Permission):
    name = _('销假(分院管理员)')
    need_permissions=('SchoolAttendance.undo_record_admin',)
    def get_context(self, request, *args, **kwargs):
        # TODO 需要进行管理员身份验证
        record = models.Record.objects.get(id=request.params.record_id)
        record.manager=request.user
        record.save()

    class Meta:
        param_fields = (
            ('record_id', fields.CharField(label=_('考勤记录ID'), max_length=8)),
        )


@site
class InzaoqianExcel(CoolBFFAPIView):
    name = _('导入早签数据')
    # TODO 需要进行管理员身份验证  导入大量的情况有问题
    need_permissions=('SchoolAttendance.undo_record_admin',)

    def get_context(self, request, *args, **kwargs):
        rows = excel_to_list(request)
        error_list=[]
        for row in rows:
            username = row[0]
            name = row[1]
            str_time = row[3]
            if username == None or str_time == None:
                continue
            
            is_header = username.find('考勤') != -1 or username.find('统计') != -1 or username.find('员工号') != -1 or username.find('考勤') != -1
            if not (username == None or name == None or str_time == None) and not is_header:
                try:
                    u = User.objects.get(username=username)
                    try:
                        str_time = datetime.datetime.strptime(str_time,'%Y/%m/%d')
                        
                        d = {
                            'rule_str':'早签',
                            'student_approved':u,
                            'score':1,
                            'grade_str':u.studentinfo.grade.name,
                            'star_time':str_time
                        }

                        try:
                            d['rule'] = models.RuleDetails.objects.get(name='早签')
                        except:
                            pass
                        
                        record,flg = models.Record.objects.get_or_create(**d)
                        record.worker =  request.user
                        record.save()
                    except:
                        error_list.append({
                            'username':username,
                            'name':name,
                            'str_time':str_time,
                            'message':'导入记录失败'
                        })
                except:
                    error_list.append({
                        'username':username,
                        'name':name,
                        'str_time':str_time,
                        'message':'用户不存在'
                    })


        return error_list

    class Meta:
        param_fields = (
            ('file',fields.FileField(label=_('Excel文件'))),
        )

@site
class TaskExecutor(Permission):
    name = _('工作者获取任务')
    response_info_serializer_class = serializers.TaskExecutor

    def get_context(self, request, *args, **kwargs):
        tasks = models.TaskPlayer.objects.filter(
            user=request.user, task__is_open=True
        )
        return serializers.TaskExecutor(tasks,many=True, request=request).data

@site
class knowingExcelOut(TaskBase):
    name = _('查寝当天数据导出')
    response_info_serializer_class = serializers.TaskRecordExcelSerializer

    def check_api_permissions(self, request, *args, **kwargs):
        pass

    def get_context(self, request, *args, **kwargs):
        get_token_by_user(request)
        task = self.get_task_by_user()
        now = datetime.date.today()
        records = models.Record.objects.filter(
            task=task,
            manager=None,
            star_time__date=datetime.date(now.year, now.month, now.day),
        )
        if not records:
            return JsonResponse({"state": "5000", "msg": "没有数据"})
        ser_records = serializers.TaskRecordExcelSerializer(
            instance=records, many=True
        ).data
        return out_knowing_data(ser_records)
    class Meta:
        param_fields = (
            ('token', fields.CharField(label=_('token'))),
        )
@site
class OutData(CoolBFFAPIView):
    name = _('筛选导出记录情况')

    def get_context(self, request, *args, **kwargs):
        ret = {}
        # 获取用户所属分院
        # TODO 优化时间查询默认值

        username = request.params.username
        start_date = request.params.start_date
        end_date = request.params.end_date
        end_date = datetime.datetime(
            end_date.year, end_date.month, end_date.day, 23, 59, 59
        )

        # 筛选条件
        q1 = Q(manager__isnull=True)
        q2 = Q(star_time__range=(start_date, end_date))
        q3 = (
            Q(student_approved=User.objects.get(username=username))
            if username != None
            else q1
        )

        records = (
            models.Record.objects.filter(q2 & q1 & q3)
            .values(
                grade=F('grade_str'),
                name=F('student_approved__userinfo__name'),
            )
            .annotate(
                rule=Concat('rule_str'),
                score_onn=Concat('score'),
                score=Sum('score'),
                time=Concat('star_time'),
                rule_type=Concat('rule__rule__codename'),
            )
            .values(
                'grade',
                'name',
                'rule_type',
                'rule',
                'score_onn',
                'score',
                'time',
                usernames=F('student_approved__username'),
            )
        )

        for record in records:
            rule_type = record['rule_type'].split(',')
            rule = record['rule'].split(',')
            score_onn = record['score_onn'].split(',')
            time = record['time'].split(',')

            # 根据rule_type 把违纪情况拆分合并为 分数1 分数1 分数1 原因1 原因1 原因1
            for index in range(0, len(rule_type)):
                type_ = rule_type[index]

                if not type_ + 'score' in record:
                    record['0#001score'] = 0
                    record['0#002score'] = 0
                    record['0#003score'] = 0
                    record['0#004score'] = 0
                    record['0#005score'] = 0
                if not type_ + 'rule' in record:
                    record['0#001rule'] = ''
                    record['0#002rule'] = ''
                    record['0#003rule'] = ''
                    record['0#004rule'] = ''
                    record['0#005rule'] = ''

                # 分数累加
                record[type_ + 'score'] += int(score_onn[index])

                # 规则拼接
                t = time[index][5:10]
                record[type_ + 'rule'] += t + "：" + str(rule[index]) + '\r\n'
            rule_str = record[type_ + 'rule']
            record[type_ + 'rule'] = rule_str[0:len(rule_str)-2]

            del record['time']
            del record['rule_type']
            del record['rule']
            del record['score_onn']

        return at_all_out_xls(records)


    class Meta:
        now = datetime.datetime.now()
        t = datetime.datetime(now.year, now.month, now.day)
        t = datetime.datetime.strftime(t, "%Y-%m-%d")
        param_fields = (
            ('username',fields.CharField(label=_('用户名'),default=None)),
            ('start_date',fields.DateField(label=_('开始日期'),default=t)),
            ('end_date',fields.DateField(label=_('结束日期'),default=t)),
        )
@site
class Rule(CoolBFFAPIView):
    name = _('获取规则')

    def get_context(self, request, *args, **kwargs):
        codename = request.params.codename
        rule = models.Rule.objects.get(codename=codename)
        data = rule.ruledetails_set.all().values('id', 'name', 'parent_id', 'score')
        return list(data)
    class Meta:
        param_fields = (
            ('codename',fields.CharField(label=_('规则编号'))),
        )
@site
class SubmitLateDiscipline(TaskBase):
    name = _('晚自修考勤 违纪提交')

    def get_context(self, request, *args, **kwargs):
        self.get_task_player_by_user()
        self.is_open()

        username = request.params.username
        role_score = request.params.role_score
        role_name = request.params.role_name
        rule_id_list = request.params.rule_id_list
        user = User.objects.get(username=username)

        if rule_id_list:
            for id in rule_id_list:
                rule = models.RuleDetails.objects.get(id=id)
                d = {
                'task' : self.task,
                'rule_str' : rule.name,
                'score' : rule.score,
                'rule' : rule,
                'grade_str' : user.studentinfo.grade.name,
                'student_approved' : user,
                'worker' : request.user,
                }
                models.Record.objects.create(**d)
        elif role_name:
            # 自定义规则提交
            rule_obj = models.Rule.objects.get(codename='0#003')
            rule_obj,f = models.RuleDetails.objects.get_or_create(name='其他违纪',defaults={'rule':rule_obj,'score':1})
            d = {
              'task' : self.task,
              'rule_str' : role_name,
              'rule' : rule_obj,
              'score' : role_score,
              'grade_str' : user.studentinfo.grade.name,
              'student_approved' : user,
              'worker' : request.user,
            }
            models.Record.objects.create(**d)
    class Meta:
        param_fields = (
            ('username',fields.CharField(label=_('用户名'))),
            ('role_name',fields.CharField(label=_('自定义规则名称'),default=None)),
            ('role_score',fields.CharField(label=_('自定义规则分数'),default=None)),
            ('rule_id_list',fields.ListField(label=_('规则ID列表'),default=None)),
        )
@site
class SubmitLate(TaskBase):
    name = _('晚自修考勤 点名提交')

    def get_context(self, request, *args, **kwargs):
        # 获取参数
        self.get_task_player_by_user()
        self.is_open()
        flg = request.params.flg
        rule_id = request.params.rule_id
        user_list = request.params.user_list
        # 获取规则
        rule = models.RuleDetails.objects.get(id=int(rule_id))
        for u in user_list:
            user = User.objects.get(username=u)
            call,status = models.UserCall.objects.get_or_create(task=self.task,user=user,rule=rule)
            # 判断是不是本次任务第一次点名
            if call.flg == None:
                call.flg = flg
                call.save()
                # 写入考勤记录
                if not flg:
                    d = {
                        'task':self.task,
                        'rule_str':rule.name,
                        'score':rule.score,
                        'rule':rule,
                        'grade_str':user.studentinfo.grade.name,
                        'student_approved':user,
                        'worker':request.user,
                    }
                    models.Record.objects.create(**d)

    class Meta:
        param_fields = (
            ('flg',fields.BooleanField(label=_('是否第一次点名'))),
            ('rule_id',fields.CharField(label=_('规则ID'))),
            ('user_list',fields.ListField(label=_('被记录用户列表'))),
        )
@site
class SubmitKnowing(TaskBase):
    name = _('寝室考勤 点名提交')

    def get_context(self, request, *args, **kwargs):

        # 获取参数
        self.get_task_player_by_user()
        self.is_open()


        room_id = request.params.room_id
        user_list = request.params.user_list

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

        for d in user_list:
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
                    star_time__date=t, worker=request.user, student_approved=user
                ).update(manager=request.user, rule_str='查寝：误操作撤销')

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
                    'worker': request.user,
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
    class Meta:
        param_fields = (
            ('room_id',fields.CharField(label=_('房间ID'))),
            ('user_list',fields.ListField(label=_('被记录用户列表'))),
        )
@site
class KnowingStoreyInfo(TaskBase):
    name = _('晚查寝-楼工作数据')

    def get_context(self, request, *args, **kwargs):
        self.get_task()
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


@site
class KnowingRoomInfo(TaskBase):
    name = _('晚查寝-层工作数据')

    def get_context(self, request, *args, **kwargs):
        self.get_task()
        d = {"0": "dorm_status", "1": "health_status"}
        floor_id = request.params.floor_id
        if not floor_id:
            return
        rooms = models.Room.objects.filter(floor_id=floor_id).values(
            'id', 'name', 'health_status', 'dorm_status'
        )
        for room in rooms:
            room['status'] = room[d[self.task.types]]
            del room['health_status']
            del room['dorm_status']
        return list(rooms)

    class Meta:
        param_fields = (
            ('floor_id',fields.CharField(label=_('楼层ID'))),
        )
@site
class KnowingStudentRoomInfo(TaskBase):
    name = _('晚查寝-房间工作数据')

    def get_context(self, request, *args, **kwargs):
        self.get_task()
        room_id = request.params.room_id

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

    class Meta:
        param_fields = (
            ('room_id',fields.CharField(label=_('房间ID'))),
        )
@site
class StudentDisciplinary(CoolBFFAPIView):
    name = _('学生查看公告')
    response_info_serializer_class = serializers.StudentDisciplinary
    def get_context(self, request, *args, **kwargs):
        # TODO 优化为仅支持查看本学院的情况
        task_id_list = models.Task.objects.filter(types='0').values_list('id', flat=True)
        now = datetime.datetime.now()  # ,star_time__date=datetime.date(now.year, now.month,now.day))
        records = models.Record.objects.filter(
            task__in=task_id_list,
            manager=None,
            star_time__date=datetime.date(now.year, now.month, now.day),
        )
        return  serializers.StudentDisciplinary(records, many=True).data

@site
class LateClass(TaskBase):
    name =_('晚自修数据')

    def get_context(self, request, *args, **kwargs):
        type_ = int(request.params.type)
        task_id = request.params.task_id
        task = models.Task.objects.get(id=task_id)
        if type_ == 0:
            grades = (
                models.Task.objects.get(id=task_id).grades.all().values('id', 'name')
            )
            return list(grades)
        elif type_ == 1:
            class_id = request.params.class_id
            rule_id = request.params.rule_id
            users = SchoolInformationModels.Grade.objects.get(id=class_id).get_users()
            rule = models.RuleDetails.objects.get(id=rule_id)
            l = []  # TODO 性能影响
            for u in users:
                call, flg = models.UserCall.objects.get_or_create(
                    task=task, user=u, rule=rule
                )
                d = {}
                d['username'] = u.username
                d['name'] = u.userinfo.name
                d['flg'] = call.flg
                l.append(d)
            return l

    class Meta:
        param_fields = (
            ('rule_id',fields.CharField(label=_('规则ID'),default=None)),
            ('class_id',fields.CharField(label=_('班级ID'),default=None)),
            ('type',fields.CharField(label=_('0 # 获取任务绑定的班级 1 # 获取班级名单附带学生多次点名情况'))),
        )

@site
class RecordQuery(CoolBFFAPIView):
    name = _('考勤查询')

    def get_context(self, request, *args, **kwargs):
        username = request.params.username
        start_date = request.params.start_date
        end_date =request.params.end_date
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        records = models.Record.objects.filter(
            star_time__range=(start_date, end_date), manager__isnull=True
        )

        if username:
            try:
                user = User.objects.get(
                    Q(username=username) | Q(userinfo__name=username)
                )
                records = records.filter(student_approved=user)
            except:
                records = []

        pg = RecordQueryrPagination()
        page_roles = pg.paginate_queryset(queryset=records, request=request, view=self)
        ser = serializers.RecordQuery(instance=page_roles, many=True).data
        return {"total": len(records), "results": ser, "page_size": pg.page_size}

    class Meta:
        param_fields = (
            ('username',fields.CharField(label=_('用户名'),default=None)),
            ('start_date',fields.CharField(label=_('开始时间'))),
            ('end_date',fields.CharField(label=_('结束时间'))),
        )


urls = site.urls
urlpatterns = site.urlpatterns
