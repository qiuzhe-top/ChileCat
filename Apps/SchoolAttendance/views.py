'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-07-06 20:54:59
Description: 
'''
from os import name
from django.utils import tree
from core.excel_utils import at_all_out_xls, out_knowing_data
import datetime
from typing import List
from django.db.models import manager
from django.db.models.aggregates import Count, Sum

from django.db.models.manager import Manager
from django.db.models.query_utils import Q
from Apps.SchoolAttendance.service.task import TaskManage
from Apps.SchoolInformation import models as SchoolInformationModels
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from cool.views import (
    CoolAPIException,
    CoolBFFAPIView,
    ErrorCode,
    ViewSite,
    param,
    utils,
)
from django.utils.translation import gettext_lazy as _

# Create your views here.
from rest_framework.views import APIView
# from .service.knowing import knowing
from django.contrib.auth.models import User
from . import models, serializers
from .service import knowing, health, late
from itertools import chain
import json
from rest_framework import fields


'''
SchoolAttendance

类型 任务

TaskSwitch
任务开启

TaskLateClear
清除晚自习任务状态
TaskKnowingClear
清除查寝任务状态

LateScheduling
scheduling
排班

task_roomInfo
获取任务数据

submit
任务提交

condition
查看考勤工作情况

undo_record
销假

Rule
获取规则

in_zaoqian_excel
导入早签数据

progress
查看考勤进度

out_data
数据导出

storey
晚查寝-楼工作数据

room
晚查寝-层工作数据

room_students
晚查寝-房间工作数据

StudentDisciplinary
考勤公告

LateClass
晚自修-管理的班级  班级内的学生
'''

site = ViewSite(name='SchoolInformation', app_name='SchoolInformation')

@site
class TaskObtain(CoolBFFAPIView):
    name = _('获取任务')
    response_info_serializer_class = serializers.TaskAdmin

    def get_context(self, request, *args, **kwargs):
        is_type = request.params.type
        task = models.Task.objects.filter(types=is_type)
        if task.exists():
            return serializers.TaskAdmin(task, request=request).data
    class Meta:
        param_fields = (
            ('type', fields.CharField(label=_('任务类型 0晚查寝/1查卫生/2晚自修'), max_length=1)),
        )
# @site
# class TaskSwitch(CoolBFFAPIView):
#     name = _('开启/关闭任务')
#     response_info_serializer_class = serializers

#     def get_context(self, request, *args, **kwargs):
#         id = request.data['id']
#         task = models.Task.objects.get(id=id)
#         task.is_open = not task.is_open
#         flg = task.is_open
#         task.save()
#         return serializers.XX.json()


#     class Math:
#         param_fields = ('username', fields.CharField(label=_('用户名')))
# @site
# class TaskRest(CoolBFFAPIView):
#     name = _('重置任务状态')
#     response_info_serializer_class = serializers

#     def get_context(self, request, *args, **kwargs):
#         '''清除任务状态
#             request:
#                 id:1 # 任务ID
#         '''
#         ret = {}
#         try:
#             id = int(request.data.get('task_id'))
#         except:
#             print('参数获取错误')
#             return JsonResponse(ret)
            
#         task = models.Task.objects.get(id=id)

#         message = TaskManage(task).clear_task()

#         ret['message'] = message
#         ret['code'] = 2000
#         return serializers.XX.json()


#     class Math:
#         param_fields = ('username', fields.CharField(label=_('用户名')))
# @site
# class Scheduling(CoolBFFAPIView):
#     name = _('获取班表')
#     response_info_serializer_class = serializers

#     def get_context(self, request, *args, **kwargs):
#         id = request.GET['id']
#         roster = models.Task.objects.get(id=int(id)).roster
#         return serializers.XX.json()


#     class Math:
#         param_fields = ('username', fields.CharField(label=_('用户名')))

# @site
# class SchedulingUpdate(CoolBFFAPIView):
#     name = _('修改班表')
#     response_info_serializer_class = serializers

#     def get_context(self, request, *args, **kwargs):
#         '''更改班表
#             request：
#                 id: 任务id
#                 roster: 对应班表
#         '''
#         ret = {}
#         roster = request.data['roster']
#         id = request.data['id']
#         task = models.Task.objects.get(id=id)

#         message = TaskManage(task).scheduling(roster)
#         ret['message'] = message
#         ret['code'] = 2000
#         ret['data'] = roster
#         return serializers.XX.json()


#     class Math:
#         param_fields = ('username', fields.CharField(label=_('用户名')))

# @site
# class Condition(CoolBFFAPIView):
#     name = _('考勤工作情况')
#     response_info_serializer_class = serializers

#     def get_context(self, request, *args, **kwargs):
#         '''查看当天考勤工作情况
#             request:
#                 task_id:2 # 任务id
#             response:
#                 [
#                     {
#                         user_id:2 # 用户ID
#                         name: 张三 
#                     }
#                 ]
#         权限判断
#         '''
#         ret = {}
#         task_id = request.GET['task_id']
#         task = models.Task.objects.get(id=task_id)

#         data = TaskManage(task).condition()
#         ret['message'] = 'message'
#         ret['code'] = 2000
#         ret['data'] = data
#         return serializers.XX.json()


#     class Math:
#         param_fields = ('username', fields.CharField(label=_('用户名')))
# @site
# class UndoRecord(CoolBFFAPIView):
#     name = _('销假')
#     response_info_serializer_class = serializers

#     def get_context(self, request, *args, **kwargs):
#         '''销假
#             request：
#                record_id:213 # 考勤记录id
#         '''
#         ret = {}
#         record_id = request.data['record_id']
#         task_id = request.data['task_id']
#         task = models.Task.objects.get(id=task_id)
#         data = TaskManage(task).undo_record(record_id,request.user)
#         ret['message'] = data
#         ret['code'] = 2000
#         return serializers.XX.json()


#     class Math:
#         param_fields = ('username', fields.CharField(label=_('用户名')))
# @site
# class UndoRecordAdmin(APIView):
#     name = _('考勤汇总销假')
#     response_info_serializer_class = serializers

#     def get_context(self, request, *args, **kwargs):
#         '''考勤汇总销假
#             request：
#                record_id:213 # 考勤记录id
#         '''
#         ret = {}
#         # TODO 进行身份验证
#         record_id = request.data['record_id']
#         record = models.Record.objects.get(id=record_id)
#         record.manager=request.user
#         record.save()
#         ret['message'] = '操作成功'
#         ret['code'] = 2000
#         return JsonResponse(ret)
# @site
# class InZaoqianExcel(CoolBFFAPIView):
#     name = _('导入早签数据')
#     response_info_serializer_class = serializers

#     def get_context(self, request, *args, **kwargs):
#         ret = TaskManage().in_zaoqian_excel(request)
#         return serializers.XX.json()


#     class Math:
#         param_fields = ('username', fields.CharField(label=_('用户名')))

# @site
# class TaskObtain(CoolBFFAPIView):
#     name = _('获取任务')
#     response_info_serializer_class = serializers

#     def get_context(self, request, *args, **kwargs):

#         return serializers.XX.json()


#     class Math:
#         param_fields = ('username', fields.CharField(label=_('用户名')))


from django.db.models import Aggregate

class Msum(Aggregate):
    # Supports SUM(ALL field).
    function = 'SUM'
    template = '%(function)s(%(all_values)s%(expressions)s)'
    allow_distinct = False

    def __init__(self, expression, all_values=False, **extra):
        # print(self, expression, all_values, **extra)
        super().__init__(
            expression,
            all_values='ALL ' if all_values else '',
            **extra
        )
        # return "123"
from django.db.models import Aggregate, CharField

# 自定义聚合函数的名字
class Concat(Aggregate):  # 写一个类继承Aggregate，
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            arg_joiner="-",
            **extra)
from django.db.models import F
class OutData(APIView):
    API_PERMISSIONS = ['进入结果','get']
    def get(self, request, *args, **kwargs):
        '''导出今日记录情况
            request:
                id:任务ID
        '''
        ret = {}
        # 获取用户所属分院
        # TODO 优化时间查询默认值
        now = datetime.datetime.now()
        t = datetime.datetime(now.year,now.month,now.day)
        t = datetime.datetime.strftime(t,"%Y-%m-%d")
        start_date = request.GET.get('start_date',t)
        end_date = request.GET.get('end_date',t)
        username = request.GET.get('username','')

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date = datetime.datetime(end_date.year, end_date.month, end_date.day,23,59,59)
        q1 = Q(manager__isnull=True)
        q2 = Q(star_time__range=(start_date, end_date))
        q3 = Q(student_approved = User.objects.get(username=username)) if len(username) > 0 else q1
     
        records = models.Record.objects.filter(q2 & q1 & q3).values(
                    grade=F('grade_str'),
                    name=F('student_approved__userinfo__name'),
                    # rule_=F('rule__rule__name'),
                ).annotate(
                    rule=Concat('rule_str'),
                    score_onn=Concat('score'),
                    score=Sum('score'),
                    time=Concat('star_time'),
                    rule_type=Concat('rule__rule__codename'),
                ).values(
                    'grade',
                    'name',
                    'rule_type',
                    'rule',
                    'score_onn',
                    'score',
                    'time',
                    usernames=F('student_approved__username'),
                )
        
        for record in records:
            rule_type = record['rule_type'].split(',')
            rule = record['rule'].split(',')
            score_onn = record['score_onn'].split(',')
            time = record['time'].split(',')

            # 根据rule_type 把违纪情况拆分合并为 分数1 分数1 分数1 原因1 原因1 原因1
            for index in range(0,len(rule_type)):
                type_ = rule_type[index]

                if not type_+'score' in record:
                    record['0#001score'] = 0
                    record['0#002score'] = 0
                    record['0#003score'] = 0
                    record['0#004score'] = 0
                    record['0#005score'] = 0
                if not type_+'rule' in record:
                    record['0#001rule'] = ''
                    record['0#002rule'] = ''
                    record['0#003rule'] = ''
                    record['0#004rule'] = ''
                    record['0#005rule'] = ''

                # 分数累加
                record[type_+'score'] += int(score_onn[index])

                # 规则拼接
                t = time[index][5:10]
                record[type_+'rule'] += t + ":" + str(rule[index]) + ','
         
            del record['time']
            del record['rule_type']
            del record['rule']
            del record['score_onn']
            # print(record)
        # return JsonResponse({})
        return at_all_out_xls(records)

class knowingExcelOut(APIView):
    API_PERMISSIONS = ['查寝当天数据导出']
    def get(self, request, *args, **kwargs):
        '''查寝当天数据导出
        '''

        task_id = request.GET.get('task_id',False)
        if not task_id:
            return JsonResponse(
                {"state": "5000", "msg": "no role"}
            )
        task = models.Task.objects.get(id=task_id)

        time_get = datetime.date.today()

        records = models.Record.objects.filter(Q(star_time__date=time_get),task=task)
        if not records:
            return JsonResponse(
                {"state": "5000", "msg": "no data  bacak"}
            )
        ser_records = serializers.TaskRecordExcelSerializer(
            instance=records, many=True).data
            
        return out_knowing_data(ser_records)

class TaskExecutor(APIView):
    API_PERMISSIONS = ['工作者获取任务','*get']
    
    def get(self, request, *args, **kwargs):
        '''工作人员获取任务 
            response:
                [{
                    id:2                    # 任务ID
                    title:智慧彩云 晚查寝    # 名称
                    builder_name:张三       # 创建者姓名
                    is_finish:true          # 是否完成任务
                    type:'0'                # 任务类型
                },]
        '''
        ret = {}
        tasks = models.TaskPlayer.objects.filter(user=request.user,is_admin=False,task__is_open=True)
        ser = serializers.TaskExecutor(instance=tasks,many=True).data
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = ser
        return JsonResponse(ret)


class Rule(APIView):
    API_PERMISSIONS = ['规则','*get']

    def get(self, request, *args, **kwargs):
        '''获取规则
            request:
                codename: 规则编号
            response:
                list:[{
                    id:规则ID
                    name:规则名称
                    parent_id:父级ID
                }]
        '''
        ret = {}
        codename = request.GET['codename']
        rule = models.Rule.objects.get(codename=codename)
        data = rule.ruledetails_set.all().values('id','name','parent_id','score')
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = list(data)
        return JsonResponse(ret)


class Submit(APIView):
    API_PERMISSIONS=['考勤提交','*post']
    def post(self, request, *args, **kwargs):
        '''考勤提交
            request:
                task_id: 2               # 任务ID
                type: 0/1           # 提交类型 0=> 考勤提交 1=>执行人确认任务完成
                data:
                    rule_id:[1,2,3]     # 规则的ID列表
                    user_id:2           # 用户ID
                    flg :               # 点名状态
                    room_id:20          # 寝室ID
        '''
        ret = {'message': '', 'code': 2000, 'data': 'data'}
        # 获取参数
        task_id = request.data['task_id']
        data = request.data['data']
        type_ = request.data['type']
        # 获取任务
        task = models.Task.objects.get(id=task_id)
        n = models.TaskPlayer.objects.filter(task=task,user=request.user,is_admin=False).count()

        if n <= 0:
            ret['code'] = 4000
            ret['message'] = '未知考勤'
            return JsonResponse(ret)

        if type_ == 0:
            code =  TaskManage(task).submit(data,request.user)
            if code == 4001:
                ret['code'] = code
                ret['message'] = '活动未开启'
        elif type_ == 1:
            pass
        return JsonResponse(ret)

class SubmitPublic(APIView):
    def post(self, request, *args, **kwargs):
        '''通用考勤规则提交
            user_username_list:[]
            rule_id_list:[]
        '''

        pass

class TaskRoomInfo(APIView):
    API_PERMISSIONS = ['晚查寝数据','*get']
    def get(self, request, *args, **kwargs):
        '''宿舍 相关任务信息
            request:
                task_id: 1 # 任务ID
                floor_id：1 # 楼层ID
                room_id:1 # 房间ID
                type: 
                    0 # 获取楼层
                    1 # 获取房间
                    2 # 获取房间内学生状态
        根据任务ID判断是查寝还是查卫生然后返回对应处理的数据
        '''
        ret = {'message': 'message', 'code': 2000, 'data': 'data'}
        task_id = request.GET['task_id']
        types = request.GET['type']
        floor_id = request.GET.get('floor_id',-1)
        room_id = request.GET.get('room_id',-1)
        task = models.Task.objects.get(id=task_id)

        data = TaskManage(task).task_roomInfo(int(types),request.user,floor_id,room_id)
        ret['data'] = data
        return JsonResponse(ret)


# 学生查看公告
class StudentDisciplinary(APIView):
    API_PERMISSIONS=['考勤公告','get']
    def get(self,request):
        '''
        request：
        
        response 
            room_name
            student
            reason
        '''
        # TODO 支持查看本学院的情况
        task_id_list = models.Task.objects.filter(types='0').values_list('id',flat=True)
        now = datetime.datetime.now() #,star_time__date=datetime.date(now.year, now.month,now.day))
        records = models.Record.objects.filter(task__in=task_id_list,manager=None,star_time__date=datetime.date(now.year, now.month,now.day))
        ser = serializers.StudentDisciplinary(instance=records,many=True).data
        ret = {}   
        ret['code'] = 2000
        ret['message'] = '查询成功'
        ret['data'] = ser
        return JsonResponse(ret)


class LateClass(APIView):
    API_PERMISSIONS = ['晚自修数据', '*get']

    def get(self, request, *args, **kwargs):
        '''晚自修 相关数据
            request:
                task_id:任务ID
                rule_id:规则ID
                class_id:班级ID
                type: 
                    0 # 获取任务绑定的班级
                    1 # 获取班级名单附带学生多次点名情况
        '''
        ret = {}
        type_ = int(request.GET['type'])
        task_id = request.GET['task_id']
        task = models.Task.objects.get(id=task_id)
        if type_ == 0:
            grades = models.Task.objects.get(id=task_id).grades.all().values('id','name')
            ret['code'] = 2000
            ret['data'] = list(grades)
            return JsonResponse(ret)
        elif type_ == 1:
            class_id = request.GET['class_id']
            rule_id = request.GET['rule_id']
            users = SchoolInformationModels.Grade.objects.get(id=class_id).get_users()
            rule = models.RuleDetails.objects.get(id=rule_id)
            l = [] #TODO 性能影响
            for u in users:
                call,flg = models.UserCall.objects.get_or_create(task=task,user=u,rule=rule)
                d={}
                d['username'] = u.username
                d['name'] = u.userinfo.name
                d['flg'] = call.flg
                l.append(d)
            ret['message'] = 'message'
            ret['code'] = 2000
            ret['data'] = l
            return JsonResponse(ret)
class RecordQueryrPagination(PageNumberPagination):
    #每页显示多少个
    page_size = 30
    #默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数
    page_size_query_param = "size"
    #最大页数不超过10
    #max_page_size = 10
    #获取页码数的
    page_query_param = "page"

class RecordQuery(APIView):
    API_PERMISSIONS = ['考勤查询','get']
    def get(self,request):
        '''考勤记录查询接口
        request：
            start_date：2005-1-1
            end_date:2005-1-1
            username
        '''
        ret = {}

        username = request.GET.get('username',None)
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        # start_date = datetime.date(*json.loads(start_date))  # [2005,1,1]
        # end_date = datetime.date(*json.loads(end_date))
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date = datetime.datetime(end_date.year, end_date.month, end_date.day,23,59,59)
        Data = models.Record.objects.filter(
                star_time__range=(start_date, end_date),
                manager__isnull=True
            )
        # 警告:过滤具有日期的DateTimeField不会包含最后一天，因为边界被解释为“给定日期的0am”。   
        if username:
            try:
                user = User.objects.get(Q(username=username)|Q(userinfo__name=username))
                Data = Data.filter(student_approved=user)
            except:
                Data = []

        pg = RecordQueryrPagination()
        page_roles = pg.paginate_queryset(queryset=Data,request=request,view=self)
        #对数据进行序列化
        ser = serializers.RecordQuery(instance=page_roles,many=True).data
        # print(len(ser))
        ret['message'] = "获取成功"
        ret['code'] = 2000
        # page = round(len(Data) / pg.page_size)
        ret['data'] =  {"total":len(Data),"results":ser,"page_size":pg.page_size} 
        return JsonResponse(ret)
# ----------------------------------------------------------------
# class ExportExcel(APIView):
#     """导出excel """
#     API_PERMISSIONS = ['查寝Excel记录', 'get']
#     def get(self, request):
#         """给日期,导出对应的记录的excel表,不给代表今天"""
#         print("准备导出excel")
#         response = HttpResponse(content_type='application/vnd.ms-excel')
#         filename = datetime.date.today().strftime("%Y-%m-%d") + ' 学生缺勤表.xls'
#         response['Content-Disposition'] = (
#             'attachment; filename={}'.format(escape_uri_path(filename))
#         )
#         req_list = self.request.query_params
#         time_get = req_list.get('date', -1)
#         if time_get == -1:
#             time_get = date.today()
#         records = TaskRecord.objects.filter(
#             Q(manager=None) & Q(created_time__date=time_get))
#         if not records:
#             return JsonResponse(
#                 {"state": "1", "msg": "当日无缺勤"}
#             )
#         ser_records = ser.TaskRecordExcelSerializer(
#             instance=records, many=True).data
#         if ser_records:
#             ws = xlwt.Workbook(encoding='utf-8')
#             w = ws.add_sheet('sheet1')
#             w.write(0, 0, u'日期')
#             w.write(0, 1, u'楼号')
#             w.write(0, 2, u'班级')
#             w.write(0, 3, u'学号')
#             w.write(0, 4, u'姓名')
#             w.write(0, 5, u'原因')
#             row = 1
#             for i in ser_records:
#                 k = dict(i)
#                 column = 0
#                 for j in k.values():
#                     w.write(row, column, j)
#                     column += 1
#                 row += 1
#             # 循环完成
#             # path = os.getcwd()
#             # ws.save(path + "/leaksfile/{}".format(filename))
#             output = BytesIO()
#             ws.save(output)
#             output.seek(0)
#             response.write(output.getvalue())
#             print("导出excel")
#             return response


urls = site.urls
urlpatterns = site.urlpatterns
