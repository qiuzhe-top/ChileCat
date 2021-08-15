'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-08-15 10:23:08
Description: 
'''
from copy import error
from core.utils import time_end, time_start
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
class TaskObtain(PermissionView):

    name = _('获取任务')
    response_info_serializer_class = serializers.TaskObtain

    def get_context(self, request, *args, **kwargs):
        task = models.Task.objects.filter(admin=request.user, types=request.params.type).select_related('college')
        return serializers.TaskObtain(task, many=True, request=request).data

    class Meta:
        param_fields = (
            (
                'type',
                fields.CharField(
                    label=_('任务类型'), max_length=1, help_text=' 0晚查寝 1查卫生 2晚自修'
                ),
            ),
        )


@site
class TaskSwitch(TaskBase):

    name = _('开启/关闭任务')
    response_info_serializer_class = serializers.TaskSwitch

    def get_context(self, request, *args, **kwargs):
        task = self.get_task_by_user()
        task.is_open = not task.is_open
        task.save()
        return serializers.TaskSwitch(task, request=request).data


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
class TaskRestHealth(TaskBase):
    name = _('重置卫生检查任务状态')

    def get_context(self, request, *args, **kwargs):
        task = self.get_task_by_user()
        models.RoomHistory.objects.filter(task=task).update(is_health=False)



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
                            error += 1

        self.init_scheduling(user_list, roster)
        if error != 0:
            return str(error) + '个学生排班失败'

    class Meta:
        param_fields = (('roster', fields.JSONField(label=_('班表'))),)


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

        self.init_scheduling(user_list, roster_new)
        return '执行成功' + '更新' + str(len(roster_new)) + '个学生'

    class Meta:
        param_fields = (('roster', fields.JSONField(label=_('班表'))),)


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
        ).select_related('student_approved__userinfo','worker__userinfo','rule').order_by('-last_time')
        
        return serializers.ConditionRecord(records, request=request, many=True).data


@site
class UndoRecord(TaskBase):
    name = _('销假(当前任务管理员)')

    def get_context(self, request, *args, **kwargs):
        task = self.get_task_by_user()
        record = models.Record.objects.get(task=task, id=request.params.record_id)
        record.manager = request.user
        record.save()

    class Meta:
        param_fields = (
            ('record_id', fields.CharField(label=_('考勤记录ID'), max_length=8)),
        )


@site
class UndoRecordAdmin(PermissionView):
    name = _('销假(分院管理员)')
    need_permissions = ('SchoolAttendance.undo_record_admin',)

    def get_context(self, request, *args, **kwargs):
        # TODO 需要进行管理员身份验证
        record = models.Record.objects.get(id=request.params.record_id)
        record.manager = request.user
        record.save()

    class Meta:
        param_fields = (
            ('record_id', fields.CharField(label=_('考勤记录ID'), max_length=8)),
        )



@site
class TaskExecutor(PermissionView):
    name = _('工作者获取任务')
    response_info_serializer_class = serializers.TaskExecutor

    def get_context(self, request, *args, **kwargs):
        tasks = models.TaskPlayer.objects.filter(user=request.user, task__is_open=True)
        return serializers.TaskExecutor(tasks, many=True, request=request).data


@site
class knowingExcelOut(TaskBase):
    name = _('当天考勤数据导出')
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
        ).order_by('-last_time')
        if not records:
            raise CoolAPIException(ErrorCode.EXCEL_OUT_NO_DATA)
        ser_records = serializers.TaskRecordExcelSerializer(
            instance=records, many=True
        ).data
        return out_knowing_data(ser_records)

    class Meta:
        param_fields = (('token', fields.CharField(label=_('token'))),)

@site
class Rule(CoolBFFAPIView):
    name = _('获取规则')

    def get_context(self, request, *args, **kwargs):
        codename = request.params.codename
        rule = models.Rule.objects.get(codename=codename)
        data = rule.ruledetails_set.all().values('id', 'name', 'parent_id', 'score')
        return list(data)

    class Meta:
        param_fields = (('codename', fields.CharField(label=_('规则编号'))),)




@site
class SubmitLateDiscipline(SubmitBase):
    name = _('晚自修考勤 违纪提交')
    
    def get_custom_rule(self):
        '''获取自定义规则'''
        return create_custom_rule('0#003','晚自修违纪:其他情况')
            
    def submit_user_record(self,record_model,record):
        '''提交学生考勤记录'''
        # TODO 验证score是否为整型 是否超过最大分值
        try:
            record_model['score'] = record['score']
        except:
            pass
@site
class SubmitLate(SubmitBase):
    name = _('晚自修考勤 点名提交')

    def submit_user_record(self,record_model,record):
        '''提交学生考勤记录'''
        call, status = models.UserCall.objects.get_or_create(
            task=self.task, user=record_model['student_approved'], rule=record_model['rule']
        )
        # 判断是不是本次任务第一次点名
        is_none = call.flg == None
        if is_none:
            call.flg = self.request.params.flg
            call.save()
        return is_none
    class Meta:
        param_fields = (
            ('flg', fields.BooleanField(label=_('点名 在/不在'))),
        )

@site
class SubmitKnowing(SubmitBase):
    name = _('寝室考勤 点名提交')

    def get_custom_rule(self):
        '''获取自定义规则'''
        return create_custom_rule('0#001','查寝:其他情况')
            

    def updata_user_in_room(self,user,is_flg):
        ''' 学生在宿舍情况'''
        user_in_room, flg = models.TaskFloorStudent.objects.get_or_create(task=self.task, user=user)
        user_in_room.flg = is_flg
        user_in_room.save()

    def undo_record(self,record,user):
        '''撤销对学生的违纪记录'''
        self.updata_user_in_room(user,True)
        return '查寝：误操作撤销'

    def submit_user_record(self,record_model,record):
        '''提交学生考勤记录'''
        self.updata_user_in_room(record_model['student_approved'],False)
        
    class Meta:
        param_fields = (
            ('room_id', fields.CharField(label=_('房间ID'))),
        )


@site
class SubmitHealth(SubmitBase):
    name = _('寝室卫生 检查提交')

    def get_custom_rule(self):
        '''获取自定义宿舍卫生规则'''
        return  create_custom_rule('0#007','个人卫生:其他情况')

    # def get_custom_rule_personal(self):
    #     '''获取自定义宿舍个人卫生规则'''
    #     if getattr(self,'custom_rule_personal'):
    #         return self.custom_rule_personal
    #     else:
    #         self.custom_rule_personal =  create_custom_rule('0#006','宿舍卫生:其他情况')
    #         return self.custom_rule_personal

    def submit_user_record(self,record_model,record):
        '''提交学生考勤记录'''
        pass

    class Meta:
         param_fields = (
            ('room_id', fields.CharField(label=_('房间ID'))),
        )
@site
class DormStoreyInfo(TaskBase):
    name = _('楼内层列表')
    def get_context(self, request, *args, **kwargs):
        self.get_task()
        buildings = self.task.buildings.all()
        buildings_info = []
        for building in buildings:
            info = {"list": [], 'id': building.id, 'name': building.name + "号楼"}
            floors = building.floor.filter(is_open=True)
            for floor in floors:
                floor = {'id': floor.id, 'name': "第" + floor.name + "层"}
                info['list'].append(floor)
            buildings_info.append(info)
        return buildings_info


@site
class DormRoomInfo(TaskBase):
    name = _('层内房间列表')
    
    response_info_serializer_class = serializers.DormRoomInfo
    def get_context(self, request, *args, **kwargs):
        self.get_task()
        floor_id = request.params.floor_id
        rooms = models.Room.objects.filter(floor_id=floor_id)
        return serializers.DormRoomInfo(rooms,many=True,request=request).data

    class Meta:
        param_fields = (('floor_id', fields.CharField(label=_('楼层ID'))),)


@site
class DormStudentRoomInfo(TaskBase):
    name = _('房间学生 信息')
    response_info_serializer_class = serializers.DormStudentRoomInfo

    def get_context(self, request, *args, **kwargs):
        self.get_task()
        room_id = request.params.room_id
        rooms = models.StuInRoom.objects.filter(room_id=room_id).select_related('user__userinfo')
        ser =  serializers.DormStudentRoomInfo(rooms,many=True,request=request).data
        return ser
    class Meta:
        param_fields = (('room_id', fields.CharField(label=_('房间ID'))),)


@site
class StudentDisciplinary(CoolBFFAPIView):
    name = _('学生查看公告')
    response_info_serializer_class = serializers.StudentDisciplinary

    def get_context(self, request, *args, **kwargs):
        # TODO 优化为仅支持查看本学院的情况
        task_id_list = models.Task.objects.filter(types='0').values_list(
            'id', flat=True
        )
        now = (
            datetime.datetime.now()
        )  # ,star_time__date=datetime.date(now.year, now.month,now.day))
        records = models.Record.objects.filter(
            task__in=task_id_list,
            manager=None,
            star_time__date=datetime.date(now.year, now.month, now.day),
        ).order_by('-last_time')
        return serializers.StudentDisciplinary(records, many=True).data


@site
class LateClass(TaskBase):
    name = _('晚自修数据')

    def get_context(self, request, *args, **kwargs):
        self.get_task_player_by_user()
        type_ = int(request.params.type)
        if type_ == 0:
            grades = (
                self.task.grades.all().values('id', 'name')
            )
            return list(grades)
        elif type_ == 1:
            class_id = request.params.class_id
            rule_id = request.params.rule_id
            users = User.objects.filter(studentinfo__grade__id = class_id)
            calls = models.UserCall.objects.filter(user__in=users,task=self.request.task,rule_id=rule_id).select_related('user__userinfo')
            if users.count() != calls.count():
                call_list = list()
                for u in users:
                    call_list.append(UserCall(task=self.request.task,user=u,rule_id=rule_id))
                UserCall.objects.bulk_create(call_list)
                calls = models.UserCall.objects.filter(user__in=users,task=self.request.task,rule_id=rule_id).select_related('user__userinfo')
            ser = serializers.UserCallSerializer(calls,request=request,many=True).data
            return ser

    class Meta:
        param_fields = (
            ('rule_id', fields.CharField(label=_('规则ID'), default=None)),
            ('class_id', fields.CharField(label=_('班级ID'), default=None)),
            ('type', fields.CharField(label=_('0 # 获取任务绑定的班级 1 # 获取班级名单附带学生多次点名情况'))),
        )


@site
class RecordQuery(CoolBFFAPIView):
    name = _('考勤查询')

    def get_context(self, request, *args, **kwargs):
        username = request.params.username
        college_id = request.params.college_id 
        start_date = request.params.start_date
        end_date = request.params.end_date
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date = datetime.datetime(
            end_date.year, end_date.month, end_date.day, 23, 59, 59
        )
        q4 = Q(task__types__in=['2','0']) | Q(rule_str='早签') # 任务类型限制
        q5 = Q(task__college__id=college_id) # 分院
        records = models.Record.objects.filter(q4,q5,
            star_time__range=(start_date, end_date), manager__isnull=True
        ).select_related('student_approved__userinfo','worker__userinfo','rule','task__college').order_by('-last_time')

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
            ('username', fields.CharField(label=_('用户名'), default=None)),
            ('college_id', fields.IntegerField(label=_('分院ID'))),
            ('start_date', fields.CharField(label=_('开始时间'))),
            ('end_date', fields.CharField(label=_('结束时间'))),
        )


@site
class PersonalDisciplineQuery(PermissionView):
    name = _('个人违纪查询')
    response_info_serializer_class = serializers.PersonalDisciplineQuery

    def get_context(self, request, *args, **kwargs):
        data = Record.objects.filter(student_approved=request.user).select_related('worker__userinfo').order_by('-last_time')
        ser = serializers.PersonalDisciplineQuery(
            instance=data, many=True, request=request
        ).data
        return ser

@site
class InzaoqianExcel(CoolBFFAPIView):
    name = _('导入早签数据')
    # TODO 需要进行管理员身份验证  导入大量的情况有问题
    need_permissions = ('SchoolAttendance.zq_data_import',)

    def get_context(self, request, *args, **kwargs):
        rows = excel_to_list(request)
        error_list = []
        for row in rows:
            username = row[0]
            name = row[1]
            str_time = row[3]
            if username == None or str_time == None:
                continue

            is_header = (
                username.find('考勤') != -1
                or username.find('统计') != -1
                or username.find('员工号') != -1
                or username.find('考勤') != -1
            )
            f = not (username == None or name == None or str_time == None)
            if f and not is_header:
                try:
                    u = User.objects.get(username=username)
                    try:
                        str_time = datetime.datetime.strptime(str_time, '%Y/%m/%d')

                        d = {
                            'rule_str': '早签',
                            'student_approved': u,
                            'score': 1,
                            'grade_str': u.studentinfo.grade.name,
                            'star_time': str_time,
                        }

                        try:
                            d['rule'] = models.RuleDetails.objects.get(name='早签')
                        except:
                            pass

                        record, flg = models.Record.objects.get_or_create(**d)
                        record.worker = request.user
                        record.save()
                    except:
                        error_list.append(
                            {
                                'username': username,
                                'name': name,
                                'str_time': str_time,
                                'message': '导入记录失败',
                            }
                        )
                except:
                    error_list.append(
                        {
                            'username': username,
                            'name': name,
                            'str_time': str_time,
                            'message': '用户不存在',
                        }
                    )

        return error_list

    class Meta:
        param_fields = (('file', fields.FileField(label=_('Excel文件'))),)

@site
class OutData(CoolBFFAPIView):
    name = _('筛选导出记录情况')

    def get_context(self, request, *args, **kwargs):
        ret = {}
        # 获取用户所属分院
        # TODO 优化时间查询默认值

        username = request.params.username
        college_id = request.params.college_id
        start_date = request.params.start_date
        end_date = request.params.end_date
        end_date = datetime.datetime(
            end_date.year, end_date.month, end_date.day, 23, 59, 59
        )

        # 筛选条件
        q1 = Q(manager__isnull=True) # 是否销假
        q2 = Q(star_time__range=(start_date, end_date)) # 时间
        q3 = (
            Q(student_approved=User.objects.get(username=username))
            if username != None
            else q1
        ) # 是否名称搜索
        q4 = Q(task__types__in=['2','0']) | Q(rule_str='早签') # 任务类型限制
        q5 = Q(task__college__id=college_id) # 分院

        records = (
            models.Record.objects.filter(q2 & q1 & q3 & q4 & q5)
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
                # 'task__types',
                'score_onn',
                'score',
                'time',
                usernames=F('student_approved__username'),
            )
        )
        # for record in records:
        #     print(record)
        # return 
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
                    # record['0#006score'] = 0
                    # record['0#007score'] = 0
                if not type_ + 'rule' in record:
                    record['0#001rule'] = ''
                    record['0#002rule'] = ''
                    record['0#003rule'] = ''
                    record['0#004rule'] = ''
                    record['0#005rule'] = ''
                    # record['0#006rule'] = ''
                    # record['0#007rule'] = ''

                # 分数累加
                record[type_ + 'score'] += int(score_onn[index])

                # 规则拼接
                t = time[index][5:10]
                record[type_ + 'rule'] += t + "：" + str(rule[index]) + '\r\n'
            rule_str = record[type_ + 'rule']
            record[type_ + 'rule'] = rule_str[0 : len(rule_str) - 2]

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
            ('username', fields.CharField(label=_('用户名'), default=None)),
            ('college_id', fields.IntegerField(label=_('分院ID'), default=None)),
            ('start_date', fields.DateField(label=_('开始日期'), default=t)),
            ('end_date', fields.DateField(label=_('结束日期'), default=t)),
        )


urls = site.urls
urlpatterns = site.urlpatterns
