'''
Author: 邹洋
Date: 2021-05-20 08:37:12
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-07-15 13:22:16
Description: 
'''
import datetime

from Apps.SchoolAttendance.pagination import RecordQueryrPagination
from Apps.SchoolAttendance.service.task import TaskManage
from Apps.SchoolInformation import models as SchoolInformationModels
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, ViewSite
from core.excel_utils import at_all_out_xls, out_knowing_data
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
from rest_framework.pagination import PageNumberPagination

from . import models, serializers

site = ViewSite(name='SchoolInformation', app_name='SchoolInformation')

@site
class TaskObtain(CoolBFFAPIView):

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
    name = _('重置晚自习任务状态')

    def get_context(self, request, *args, **kwargs):
        task = self.get_task_by_user()
        models.UserCall.objects.filter(task=task).update(flg=None)



@site
class Scheduling(TaskBase):
    name = _('获取班表')

    def get_context(self, request, *args, **kwargs):
        return self.get_task_by_user().roster


@site
class SchedulingUpdateKnowing(TaskBase):
    name = _('修改查寝班表')

    def get_context(self, request, *args, **kwargs):
    
        roster = request.params.roster
        user_list = []
        for item in roster:
            for layer in item['layer_list']:
                for user in layer['user']:
                    if len(item['title'][:1]) != 0 and len(user['username']) != 0:
                        # 当前工作用户   # TODO 如果用户查找失败怎么处理
                        u = User.objects.get(username=user['username'])
                        user_list.append(u)

        self.init_scheduling(user_list,roster)


    class Meta:
        param_fields = (
            ('task_id', fields.CharField(label=_('任务id'), max_length=8)),
            ('roster', fields.CharField(label=_('班表'), max_length=8)),
        )


@site
class SchedulingUpdateLate(TaskBase):
    name = _('修改晚自习班表')

    def get_context(self, request, *args, **kwargs):
    
        roster = request.params.roster
        user_list = []
        roster_new = []
        # 从班表里面获取用户
        for item in roster:
            u = User.objects.filter(username=item['username'])
            if len(u) == 1:
                user_list.append(u[0])
                roster_new.append(item)

        self.init_scheduling(user_list,roster_new)
        
        return '执行成功' + '更新' + str(len(roster_new)) + '个学生' 


    class Meta:
        param_fields = (
            ('task_id', fields.CharField(label=_('任务id'), max_length=8)),
            ('roster', fields.CharField(label=_('班表'), max_length=8)),
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
        return serializers.ConditionRecord(records, request=request).data
        

@site
class UndoRecord(TaskBase):
    name = _('销假(必须为任务管理员)')

    def get_context(self, request, *args, **kwargs):
        task = self.get_task_by_user()
        record_id = request.params.record_id
        record = models.Record.objects.get(task=task,id=record_id)
        record.manager=request.user
        record.save()

    class Meta:
        param_fields = (
            ('record_id', fields.CharField(label=_('考勤记录ID'), max_length=8)),
            ('task_id', fields.CharField(label=_('任务id'), max_length=8)),
        )
        
@site
class UndoRecordAdmin(TaskBase):
    name = _('销假(任意任务)')

    def get_context(self, request, *args, **kwargs):
        # TODO 需要进行管理员身份验证
        record_id = request.params.record_id
        record = models.Record.objects.get(id=record_id)
        record.manager=request.user
        record.save()

    class Meta:
        param_fields = (
            ('record_id', fields.CharField(label=_('考勤记录ID'), max_length=8)),
        )


@site
class InZaoqianExcel(CoolBFFAPIView):
    name = _('导入早签数据')

    def get_context(self, request, *args, **kwargs):
        file = request.params.file
        
        wb = load_workbook(file,read_only=True)

        error_list=[]
        for rows in wb:
            for row in rows:#遍历行
                username = row[0].internal_value
                name = row[1].internal_value
                str_time = row[3].internal_value
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
class TaskExecutor(CoolBFFAPIView):
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

    def get_context(self, request, *args, **kwargs):
        task = self.get_task_by_user()
        time_get = datetime.date.today()
        records = models.Record.objects.filter(Q(star_time__date=time_get), task=task)
        if not records:
            return JsonResponse({"state": "5000", "msg": "no data  bacak"})
        ser_records = serializers.TaskRecordExcelSerializer(
            instance=records, many=True
        ).data
        return out_knowing_data(ser_records)


@site
class OutData(CoolBFFAPIView):
    name = _('导出今日记录情况')

    def get_context(self, request, *args, **kwargs):
        ret = {}
        # 获取用户所属分院
        # TODO 优化时间查询默认值
        # TODO 联调测试
        now = datetime.datetime.now()
        t = datetime.datetime(now.year, now.month, now.day)
        t = datetime.datetime.strftime(t, "%Y-%m-%d")
        start_date = request.GET.get('start_date', t)
        end_date = request.GET.get('end_date', t)
        username = request.GET.get('username', '')

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date = datetime.datetime(
            end_date.year, end_date.month, end_date.day, 23, 59, 59
        )

        # 筛选条件
        q1 = Q(manager__isnull=True)
        q2 = Q(star_time__range=(start_date, end_date))
        q3 = (
            Q(student_approved=User.objects.get(username=username))
            if len(username) > 0
            else q1
        )

        records = (
            models.Record.objects.filter(q2 & q1 & q3)
            .values(
                grade=F('grade_str'),
                name=F('student_approved__userinfo__name'),
                # rule_=F('rule__rule__name'),
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
                record[type_ + 'rule'] += t + ":" + str(rule[index]) + ','

            del record['time']
            del record['rule_type']
            del record['rule']
            del record['score_onn']
            # print(record)
        # return JsonResponse({})
        return at_all_out_xls(records)

    class Meta:
        param_fields = (
            ('username',fields.CharField(label=_('用户名'),default=None)),
            ('start_date',fields.DateField(label=_('开始日期'),default=None)),
            ('end_date',fields.DateField(label=_('结束日期'),default=None)),
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
class Submit(TaskBase):
    name = _('考勤提交')

    def get_context(self, request, *args, **kwargs):
        '''
        request:
            data:
                rule_id:[1,2,3]     # 规则的ID列表
                user_id:2           # 用户ID
                flg :               # 点名状态
                room_id:20          # 寝室ID
        '''
        ret = {'message': '', 'code': 2000, 'data': 'data'}
        # 获取参数
        data = request.parmas.data
        type_ = request.parmas.type
        # 获取任务
        task = self.get_task()
        n = models.TaskPlayer.objects.filter(
            task=task, user=request.user, is_admin=False
        ).count()

        if n <= 0:
            ret['code'] = 4000
            ret['message'] = '未知考勤'
            return ret

        if type_ == 0:
            code = TaskManage(task).submit(data, request.user)
            if code == 4001:
                ret['code'] = code
                ret['message'] = '活动未开启'
        elif type_ == 1:
            pass
        return ret

    class Meta:
        param_fields = (
            ('task_id',fields.CharField(label=_('任务ID'))),
            ('type',fields.CharField(label=_('提交类型 0=> 考勤提交 1=>执行人确认任务完成'))),
            ('data',fields.CharField(label=_('任务ID'))),
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
        floor_id = request.parmas.floor_id
        if floor_id:
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
            ('task_id',fields.CharField(label=_('任务ID'))),
            ('floor_id',fields.CharField(label=_('楼层ID'))),
        )
@site
class KnowingStudentRoomInfo(TaskBase):
    name = _('晚查寝-房间工作数据')

    def get_context(self, request, *args, **kwargs):
        self.get_task()
        room_id = request.parmas.room_id

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
            ('task_id',fields.CharField(label=_('任务ID'))),
            ('room_id',fields.CharField(label=_('房间ID'))),
        )
@site
class StudentDisciplinary(CoolBFFAPIView):
    name = _('学生查看公告')
    response_info_serializer_class = serializers.StudentDisciplinary
    def get_context(self, request):
        # TODO 支持查看本学院的情况
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
        )
        return  serializers.StudentDisciplinary(records, many=True,request=request).data

@site
class LateClass(TaskBase):
    name =_('晚自修数据')

    def get_context(self, request, *args, **kwargs):
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
            grades = (
                models.Task.objects.get(id=task_id).grades.all().values('id', 'name')
            )
            ret['code'] = 2000
            ret['data'] = list(grades)
            return ret
        elif type_ == 1:
            class_id = request.GET['class_id']
            rule_id = request.GET['rule_id']
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
            ret['message'] = 'message'
            ret['code'] = 2000
            ret['data'] = l
            return ret

    class Meta:
        param_fields = (
            ('task_id',fields.CharField(label=_('任务ID'))),
            ('rule_id',fields.CharField(label=_('规则ID'))),
            ('class_id',fields.CharField(label=_('班级ID'))),
            ('type',fields.CharField(label=_('0 # 获取任务绑定的班级 1 # 获取班级名单附带学生多次点名情况'))),
        )


class RecordQuery(CoolBFFAPIView):
    name = _('考勤查询')

    def get_context(self, request):
        '''考勤记录查询接口
        request：
            start_date：2005-1-1
            end_date:2005-1-1
            username
        '''
        ret = {}

        username = request.GET.get('username', None)
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        # start_date = datetime.date(*json.loads(start_date))  # [2005,1,1]
        # end_date = datetime.date(*json.loads(end_date))
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        end_date = datetime.datetime(
            end_date.year, end_date.month, end_date.day, 23, 59, 59
        )
        Data = models.Record.objects.filter(
            star_time__range=(start_date, end_date), manager__isnull=True
        )
        # 警告:过滤具有日期的DateTimeField不会包含最后一天，因为边界被解释为“给定日期的0am”。
        if username:
            try:
                user = User.objects.get(
                    Q(username=username) | Q(userinfo__name=username)
                )
                Data = Data.filter(student_approved=user)
            except:
                Data = []

        pg = RecordQueryrPagination()
        page_roles = pg.paginate_queryset(queryset=Data, request=request, view=self)
        # 对数据进行序列化
        ser = serializers.RecordQuery(instance=page_roles, many=True).data
        ret['message'] = "获取成功"
        ret['code'] = 2000
        # page = round(len(Data) / pg.page_size)
        ret['data'] = {"total": len(Data), "results": ser, "page_size": pg.page_size}
        return JsonResponse(ret)

    class Meta:
        param_fields = (
            ('username',fields.CharField(label=_('用户名'))),
            ('start_date',fields.CharField(label=_('开始时间'))),
            ('end_date',fields.CharField(label=_('结束时间'))),
        )

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
