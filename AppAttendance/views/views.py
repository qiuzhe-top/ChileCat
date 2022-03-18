from statistics import mode
from django.shortcuts import render
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, ViewSite
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from AppAttendance.common.configuration import *
from AppAttendance.common.launch import run_init
from core.views import *
from AppAttendance.models import *
from AppAttendance import models as AppAttendancemodels
from AppInformation.models import *
from AppAttendance import serializers
from AppAttendance.views.parent import *
from .parent import *
from .admin import *
from .worker import *
from rest_framework import fields

site = ViewSite(name='Attendance', app_name='Attendance')


# ================================================= #
# ************** 工作人员             ************** #
# ================================================= #

@site
class Condition(TaskBase):

    name = _('考勤学生记录情况')
    response_info_serializer_class = serializers.ConditionRecord

    def get_context(self, request, *args, **kwargs):
        # 开始时间和结束时间
        start_date = get_start_date()
        end_date = get_end_date()

        # 楼-层筛选
        building = request.params.building
        floor = request.params.floor
        q_floor = Q()
        if building and floor:
            query_str = building + '#' + floor
            q_floor = Q(room_str__startswith=query_str)

        records = (
            Record.objects.filter(
                q_floor,
                task=self.get_task_by_user(),
                # TODO 用户为空这个条件可以定义到父类
                manager_username=None,
                star_time__range=(start_date, end_date),
            )
            .select_related('rule')
            .order_by('-last_time')
        )
        return serializers.ConditionRecord(records, request=request, many=True).data

    class Meta:

        param_fields = (
            ('building', fields.CharField(label=_('楼'), default=None)),
            ('floor', fields.CharField(label=_('层'), default=None)),
            ('start_date', fields.DateField(label=_('开始日期'), default=None)),
            ('end_date', fields.DateField(label=_('结束日期'), default=None)),
        )


@site
class TaskExecutor(PermissionView):
    name = _('工作者获取任务')
    response_info_serializer_class = serializers.TaskExecutor

    def get_context(self, request, *args, **kwargs):
        tasks = Task.objects.filter(player__username = request.user.username, is_open=True)
        return serializers.TaskExecutor(tasks, many=True, request=request).data


@site
class Rule(CoolBFFAPIView):
    name = _('获取规则')

    def get_context(self, request, *args, **kwargs):
        codename = request.params.codename
        rule = AppAttendancemodels.Rule.objects.get(codename=codename)
        data = rule.ruledetails_set.exclude(name__endswith=CUSTOM_RULE).values(
            'id', 'name', 'parent_id', 'score'
        )
        return list(data)

    class Meta:
        param_fields = (('codename', fields.CharField(label=_('规则编号'))),)

@site
class OutExcel(CoolBFFAPIView,ExcelBase):
    name = '表格模板'

    def excel_template(self,request):
        name = request.params.name
        wb, ws = self.open_excel('Module/core/file/' + name)
        r = self.create_excel_response(name)
        return self.write_file(r,wb)

    def get_context(self, request, *args, **kwargs):
        return self.excel_template(request)

    class Meta:
        param_fields = (
            ('name', fields.CharField(label=_('名称'),default=None)),
        )

# ================================================= #
# ************** 学生基本功能         ************** #
# ================================================= #


@site
class StudentDisciplinary(CoolBFFAPIView):
    name = _('学生查看公告')
    response_info_serializer_class = serializers.StudentDisciplinary

    def get_context(self, request, *args, **kwargs):
        # TODO 优化公告筛选条件 添加学校
        # 获取晚查寝任务
        task_id_list = Task.objects.filter(types='0').values_list(
            'id', flat=True
        )
        # 获取今天
        start = get_start_date()
        end = get_end_date()
        # 筛选晚查寝记录
        records = Record.objects.filter(
            task__in=task_id_list,
            manager_username=None,
            star_time__range=(start,end),
        ).order_by('-last_time')
        return serializers.StudentDisciplinary(records, many=True).data



@site
class PersonalDisciplineQuery(PermissionView):
    name = _('个人违纪查询')
    response_info_serializer_class = serializers.PersonalDisciplineQuery

    def get_context(self, request, *args, **kwargs):
        # 查询条件 查询本人没有被核销的记录
        q_user = Q(student_approved_username=request.user.username, manager_username__isnull=True)
        data = Record.objects.filter(q_user).order_by('-last_time')
        return serializers.PersonalDisciplineQuery(instance=data, many=True, request=request).data

    class Meta:
        param_fields = (('room', fields.BooleanField(label=_('查询寝室'), default=False)),)
# run_init()
urls = site.urls
urlpatterns = site.urlpatterns + worker_urlpatterns  + admin_urlpatterns
