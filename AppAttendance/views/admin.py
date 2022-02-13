'''
Author: 邹洋
Date: 2022-01-26 13:32:21
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-13 19:55:58
Description: 考勤任务管理员所需要的接口
'''
import datetime
import json
from urllib.request import Request

from AppAttendance import serializers
from AppAttendance.common.configuration import *
from AppAttendance.common.pagination import RecordQueryrPagination
from AppAttendance.models import *
from AppAttendance.views.parent import *
# from AppInformation.models import *
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, ViewSite
from Core.common.query_methods import *
# from Core.views import 
from django.db.models import F
from django.db.models.aggregates import Sum
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import fields

site = ViewSite(name='Admin', app_name='Admin')

# ================================================= #
# ************** 考勤任务基本功能      ************** #
# ================================================= #
@site
class TaskObtain(PermissionView):
    name = _('获取任务')
    response_info_serializer_class = serializers.TaskObtain

    def get_context(self, request, *args, **kwargs):
        tasks = Task.objects.filter(types=request.params.type,admin=request.user)
        task_list = []
        # for task in tasks:
        #     admin_list = task.get_admin()
        #     if request.user.username in admin_list:
        #         task_list.append(task)
        return serializers.TaskObtain(tasks, many=True, request=request).data

    class Meta:
        param_fields = ((
            'type',
            fields.CharField(label=_('任务类型'),
                             max_length=1,
                             help_text=' 0晚查寝 1查卫生 2晚自修'),
        ), )

@site
class Scheduling(TaskBase):
    name = _('获取排版表')

    def get_context(self, request, *args, **kwargs):
        return json.loads(self.get_task_by_user().roster)

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
class UndoRecord(TaskBase, RecordBase):
    name = _('销假(当前任务管理员)')

    def get_context(self, request, *args, **kwargs):
        task = self.get_task_by_user()
        id = request.params.record_id
        record = self.get_record_by_id_task(id, task)
        self.undo_record(record, request.user.username,request.user.name)

    class Meta:
        param_fields = (
            ('record_id', fields.CharField(label=_('考勤记录ID'), max_length=8)),
        )

@site
class knowingExcelOut(TaskBase, ExcelBase):
    name = _('当天考勤数据导出')
    response_info_serializer_class = serializers.TaskRecordExcelSerializer
    header = ['日期', '楼号', '班级', '学号', '姓名', '原因','分数']

    def check_api_permissions(self, request, *args, **kwargs):
        pass

    def get_context(self, request, *args, **kwargs):
        # 导出接口添加接口验证 get_token_by_user(request)
        task = self.get_task_by_user()
        start_date = get_start_date(request)
        end_date = get_end_date(request)
        records = Record.objects.filter(
            task=task,
            manager_username=None,
            star_time__range=(start_date, end_date),
        ).order_by('-last_time')
        if not records:
            return HttpResponse('当前没有违纪记录')
        ser_records = serializers.TaskRecordExcelSerializer(
            instance=records, many=True
        ).data
        return self.download_excel(ser_records, '学生考勤表', knowingExcelOut.header, 2)

    class Meta:
        param_fields = (
            ('token', fields.CharField(label=_('token'))),
            ('start_date', fields.DateField(label=_('开始日期'), default=None)),
            ('end_date', fields.DateField(label=_('结束日期'), default=None)),
        )


# ================================================= #
# ************** 晚查寝           ************** #
# ================================================= #

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
                    if len(item['title'][:1]) != 0 and len(
                            user['username']) != 0:
                        try:
                            user_list.append(user['username'])
                        except:
                            error += 1

        self.init_scheduling(user_list, roster)
        if error != 0:
            return str(error) + '个学生排班失败'

    class Meta:
        param_fields = (('roster', fields.JSONField(label=_('班表'))), )

@site
class ModifyTaskFloorSettings(TaskBase):
    name = _('修改任务楼层设置')
   
    def get_context(self, request, *args, **kwargs):
        self.get_task_by_user()
        buildings = request.params.buildings
        self.task.buildings = json.dumps(buildings)
        self.task.save()
        return '保存成功'

    class Meta:
        param_fields = (
            ('buildings', fields.ListField(label=_('房间'), default=None)),
        )
# ================================================= #
# ************** 晚自修           ************** #
# ================================================= #
# @site
# class TaskRestLate(TaskBase):
#     name = _('重置晚自修任务状态')

#     def get_context(self, request, *args, **kwargs):
#         task = self.get_task_by_user()
#         UserCallCache().init_all_grades_call([task])


@site
class SchedulingUpdateLate(TaskBase):
    name = _('修改晚自修班表')

    def get_context(self, request, *args, **kwargs):
        roster = request.params.roster
        user_list = []
        roster_new = []

        for item in roster:
            user_list.append(item['username'])

 
        db_username_list = User.objects.filter(username__in = user_list)

        user_list = []
        for user in db_username_list:
            roster = {
                "username": user.username,
                "name": user.name,
                "tel": user.tel,
            }
            roster_new.append(roster)
            user_list.append(user.username)
        self.init_scheduling(user_list, roster_new)
        return '执行成功' + '更新' + str(len(roster_new)) + "个学生"

    class Meta:
        param_fields = (('roster', fields.JSONField(label=_('班表'))), )
@site
class UpdateRoolCall(CoolBFFAPIView, UserCallCache):
    name = _('更新所有点名名单')

    def get_context(self, request, *args, **kwargs):
        self.init_all_grades_call()


# ================================================= #
# ************** 卫生           ************** #
# ================================================= #


# ================================================= #
# ************** 权益部 管理员        ************** #
# ================================================= #
@site
class UndoRecordAdmin(PermissionView, RecordBase):
    name = _('销假(权益部)')
    need_permissions = ('AppAttendance.task_leader_quan_yi_bu', )

    def get_context(self, request, *args, **kwargs):
        #  TODO 需要进行管理员身份验证,并且只能对自己分院有效
        id = request.params.record_id
        record = self.get_record_by_id(id)
        user = request.user
        self.undo_record(record, user.username, user.name)

    class Meta:
        param_fields = (('record_id',
                         fields.CharField(label=_('考勤记录ID'), max_length=8)), )

@site
class BatchUndo(ExcelInData, RecordBase):
    name = _('批量核销')
    need_permissions = ('AppAttendance.batch_cancel_after_verification', )

    header = [
        '学号',
        '姓名',
        '原因',
        '状态',
        '记录ID',
        '核销人学号',
        '核销人姓名',
        '创建时间',
        '最后修改时间',
    ]
    def main_body(self, item, user, line):
        username = item['username']
        start_time = item['start_time']
        end_time = item['end_time']
        try:
            start_time = self.time_format_one(start_time)
            end_time = self.time_format_one(end_time)
        except:
            self.add_message('第'+str(line)+'行日期格式错误')
            return
        q1 = Q(star_time__range=(start_time, end_time))
        q2 = Q(student_approved_username=username)
        q3 = Q(task__types__in=['0', '2', '3'])
        q4 = Q(manager_username__isnull=True)
        records = Record.objects.filter(q1, q2, q3, q4)
        for record in records:
            if record.manager_username == None:
                self.undo_record(record, user.username, user.name)
                self.add_message(
                    username,
                    record.student_approved_name,
                    record.rule_str,
                    '销假完成',
                    record.id,
                )
            else:
                self.add_message(
                    username,
                    record.student_approved_name,
                    record.rule_str,
                    '已被核销',
                    record.id,
                    record.manager_username,
                    record.manager_name,
                    str(record.star_time),
                    str(record.last_time),
                )

    def get_context(self, request, *args, **kwargs):
        user = request.user
        self.init(request)

        line = 1
        for item in self.rows:
            self.main_body(item, user,line)
            line+=1

        if request.params.is_excel:

            return self.download_excel(self.message_list, '核销记录', BatchUndo.header)
        else:
            return self.message_list

    class Meta:
        param_fields = (
            ('file', fields.FileField(label=_('Excel文件'), default=None)),
            ('is_down_excel', fields.CharField(label=_('是否导出Excel'), default=False)),
        )


@site
class BatchAttendance(ExcelInData):
    name = _('批量考勤')
    need_permissions = ('AppAttendance.check_in_data_import',)

    def get_context(self, request, *args, **kwargs):
        user = request.user
        task = Task.objects.get_or_create(
            types=request.params.task_type, college=ZHJT_CODENAM
        )[0]
        rule = RuleDetails.objects.get(id=request.params.rule_id)
        self.init(request)

        # 获取所有历史早签记录
        query = Record.objects.filter(task=task, rule=rule).values(
            name=F('student_approved_username'), time=F('star_time')
        )

        db_records = []
        for q in query:
            time = q['time']
            time = str(time.year) + '/' + str(time.month) + '/' + str(time.day)
            name = q['name']
            db_records.append(name + time)

        wait_create_record = []  # 等待批量获取的记录实例
        for row in self.rows:
            username = row['username']
            try:
                time = row['time']

                if time == None:
                    self.add_message(username, time, '日期不能为空')
                    continue

                time = self.time_formatting(time)
                if (username + time) not in db_records:
                    u = self.db_users[username]
                    try:
                        star_time = datetime.datetime.strptime(time, '%Y/%m/%d')
                    except:
                        self.add_message(
                            username, self.get_name(username), time, '日期格式错误'
                        )
                        continue

                    wait_create_record.append(
                        Record(
                            rule_str=rule.name,
                            student_approved_username=u.username,
                            student_approved_name=u.name,
                            score=rule.score,
                            grade_str=u.grade,
                            star_time=star_time,
                            worker_username=user.username,
                            worker_name=user.name,
                            task=task,
                            rule=rule,
                        )
                    )
                else:
                    self.add_message(username, self.get_name(username), time, '已经存在')
            except:
                self.add_message(username, '数据异常')

        Record.objects.bulk_create(wait_create_record)

        if request.params.is_down_excel:
            return self.download_excel(self.message_list, '考勤记录')
        else:
            return self.message_list

    class Meta:
        param_fields = (
            ('file', fields.FileField(label=_('Excel文件'), default=None)),
            ('rule_id', fields.CharField(label=_('规则id'), default=None)),
            ('task_type', fields.CharField(label=_('任务类型'), default=None)),
            ('is_down_excel', fields.CharField(label=_('是否导出Excel'), default=False)),
        )

@site
class RecordQuery(CoolBFFAPIView,MultipleRecordQueryCriteria):
    name = _('考勤查询')

    def get_context(self, request, *args, **kwargs):
        records = self.query_data(request)
        records = records.select_related('rule', 'task').order_by('-last_time')
        pg = RecordQueryrPagination()
        page_roles = pg.paginate_queryset(queryset=records, request=request, view=self)
        ser = serializers.RecordQuery(instance=page_roles, many=True).data
        return {"total": len(records), "results": ser, "page_size": pg.page_size}

    class Meta:
        param_fields = (
            ('username', fields.CharField(label=_('用户名'), default=None)),
            ('college_id', fields.CharField(label=_('分院ID'))),
            ('start_date', fields.DateField(label=_('开始时间'))),
            ('end_date', fields.DateField(label=_('结束时间'))),
        )

@site
class OutData(CoolBFFAPIView, ExcelBase, MultipleRecordQueryCriteria):
    name = _('筛选导出记录情况')

    def get_context(self, request, *args, **kwargs):
        records = self.query_data(request)
        if not records:
            return HttpResponse('当前没有违纪记录')

        records = (
            records.values(
                grade=F('grade_str'),
                name=F('student_approved_name'),
            )
            .annotate(
                rule_str=Concat('rule_str'),
                score_onn=Concat('score'),
                score=Sum('score'),
                time=Concat('star_time'),
                rule_type=Concat('rule__rule__codename'),
            )
            .values(
                'grade',
                'name',
                'rule_type',
                'rule_str',
                'score_onn',
                'score',
                'time',
                usernames=F('student_approved_username'),
            )
        )
        for record in records:
            rule_type_ = record['rule_type'].split(',')
            rule_ = record['rule_str'].split(',')
            score_onn_ = record['score_onn'].split(',')
            time_ = record['time'].split(',')
            rule_02_time = {}

            if len(time_) != len(rule_):
                record['name'] += ' 异常'

            for index in range(0, len(rule_type_)):
                type_ = rule_type_[index]
                if index > len(time_) - 1:
                    break
                if not type_ + 'score' in record:
                    record[RULE_CODE_01 + 'score'] = 0
                    record[RULE_CODE_02 + 'score'] = 0
                    record[RULE_CODE_03 + 'score'] = 0
                    record[RULE_CODE_04 + 'score'] = 0
                    record[RULE_CODE_05 + 'score'] = 0
                    # record[RULE_CODE_07+'score'] = 0
                    record[RULE_CODE_08 + 'score'] = 0
                    record[RULE_CODE_09 + 'score'] = 0
                if not type_ + 'rule' in record:
                    record[RULE_CODE_01 + 'rule'] = ''
                    record[RULE_CODE_02 + 'rule'] = ''
                    record[RULE_CODE_03 + 'rule'] = ''
                    record[RULE_CODE_04 + 'rule'] = ''
                    record[RULE_CODE_05 + 'rule'] = ''
                    # record[RULE_CODE_07+'rule'] = ''
                    record[RULE_CODE_08 + 'rule'] = ''
                    record[RULE_CODE_09 + 'rule'] = ''

                # 分数累加
                record[type_ + 'score'] += float(score_onn_[index])

                t = time_[index][5:10]
                # 统计晚自修点名扣分
                if type_ == RULE_CODE_02:
                    if t not in rule_02_time.keys():
                        rule_02_time[t] = []
                    rule_02_time[t].append(rule_[index])

                # 规则拼接
                record[type_ + 'rule'] += t + ":" + str(rule_[index]) + '\r\n'

            # 计算晚自修点名扣分
            if len(rule_02_time.keys()) > 0:
                for k in rule_02_time:
                    if len(rule_02_time[k]) == 1:
                        record[RULE_CODE_02 + 'score'] += 2
                        record['score'] += 2

            rule_str = record[type_ + 'rule']
            record[type_ + 'rule'] = rule_str[0 : len(rule_str) - 2]

            del record['time']
            del record['rule_type']
            del record['rule_str']
            del record['score_onn']

        # 导出
        wb, ws = self.open_excel("/Core/file/学生考勤信息记录")
        for i in records:
            k = dict(i)
            ws.append(
                [
                    k.get('grade', ''),
                    k.get('usernames', ''),
                    k.get('name', ''),
                    # 晨点
                    k.get(RULE_CODE_08 + 'score', 0),
                    k.get(RULE_CODE_08 + 'rule', ''),
                    # 晨跑
                    k.get(RULE_CODE_09 + 'score', 0),
                    k.get(RULE_CODE_09 + 'rule', ''),
                    # 早签
                    k.get(RULE_CODE_04 + 'score', 0),
                    k.get(RULE_CODE_04 + 'rule', ''),
                    # 晚签
                    k.get(RULE_CODE_02 + 'score', 0),
                    k.get(RULE_CODE_02 + 'rule', ''),
                    # 晚自修违纪
                    k.get(RULE_CODE_03 + 'score', 0),
                    k.get(RULE_CODE_03 + 'rule', 0),
                    # 查寝
                    k.get(RULE_CODE_01 + 'score', 0),
                    k.get(RULE_CODE_01 + 'rule', ''),
                    # 课堂
                    k.get(RULE_CODE_05 + 'score', 0),
                    k.get(RULE_CODE_05 + 'rule', ''),
                    k.get('score', ''),
                ]
            )
        TIME = datetime.datetime.now()  # .strftime("%H:%M:%S")
        ws.append(['统计时间:', TIME])
        response = self.create_excel_response('学生缺勤表')
        return self.write_file(response, wb)

    class Meta:
        param_fields = (
            ('username', fields.CharField(label=_('用户名'), default=None)),
            ('college_id', fields.CharField(label=_('分院ID'), default=None)),
            ('start_date', fields.DateField(label=_('开始日期'), default=None)),
            ('end_date', fields.DateField(label=_('结束日期'), default=None)),
        )


# ================================================= #
# ************** 系统管理员        ************** #
# ================================================= #

@site
class UploadDormitoryPersonnelList(PermissionView,ExcelBase):
    name = _('上传寝室名单')
   
    def get_context(self, request, *args, **kwargs):
        data = []
        rows = self.excel_to_list(request)
        for row in rows:
            print(row)
    class Meta:
        param_fields = (
            ('username', fields.CharField(label=_('用户名'), default=None)),
        )
# # 定时任务
@site
class ResetTask(CoolBFFAPIView):
    name = _('定时任务 重置任务状态')
   
    def get_context(self, request, *args, **kwargs):
        Task.objects.all().update(is_open=False) # 关闭所有任务
        # 重置考勤缓存
        UserCallCache().update_grades_call_cache()
        DormCallCache().init_data()

class ImportRecord(ExcelBase):
    name = _('导入记录')
    def get_context(self, request, *args, **kwargs):
        pass
admin_urls = site.urls
admin_urlpatterns = site.urlpatterns
