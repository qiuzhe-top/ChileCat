from Apps.SchoolAttendance.service.task import TaskManage
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
# from .service.knowing import knowing
from django.contrib.auth.models import User
from . import models, serializers
from .service import knowing, health, late
from itertools import chain
import json

class Task(APIView):
    def get(self, request, *args, **kwargs):
        '''获取任务
            request:
                type: # 获取任务的类型
                    0 # 晚查寝
                    1 # 查卫生
                    2 # 晚自修
            response:
                [{
                    id:1 # 任务id
                    name: 智慧学院 晚查寝 
                    is_open:true # 任务开启状态
                    is_builder:true #是否是本任务创建者
                }]
        '''
        ret = {}

        is_type = request.data['type']

        user = request.user

        task = models.Task.objects.filter(
            types=is_type, user=user)

        ser1 = serializers.TaskBuilder(instance=task, many=True).data

        task_admin = models.TaskPlayer.objects.filter(
            user=user, is_admin=True)

        ser2 = serializers.TaskAdmin(instance=task_admin, many=True).data

        # FIXME(zouyang): 会产生重复任务数据 因为 创建者会把自己设置为管理员
        datas = list(chain(ser1, ser2))
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = datas
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        '''创建任务
            request:
                {
                    type: # 任务类型 参考models设计
                        0 # 晚查寝
                        1 # 查卫生
                        2 # 晚自修
                    ids:[1,5,2] # if type == 0/1 => 宿舍楼ID else 班级ID
                }
            创建任务需要判断有没有对应权限
        '''
        ret = {}
        user = request.user

        try:
            is_type = str(request.data['type'])
            ids = request.data['ids']
        except:
            ret['message'] = '请求参数异常'
            ret['code'] = 5000
            return JsonResponse(ret)

        try:
            college = user.studentinfo.grade.college
        except:
            ret['message'] = '用户没有班级'
            ret['code'] = 5000
            return JsonResponse(ret)

        dic = {
            'user': user,
            'is_open': True,
            'types': is_type,
            'college': college,
        }

        task = models.Task.objects.create(**dic)

        TaskManage().create_task(ids)

        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)


class TaskAdmin(APIView):
    def get(self, request, *args, **kwargs):
        '''获取任务管理员
            request:
                id:1 # 任务id
            response:
                [{
                    user_id:2 #用户id
                    uese_name: 张三 # 姓名
                }]
        '''

        id = int(request.GET['id'])
        task_player = models.TaskPlayer.objects.filter(
            task=id, is_admin=True)
        ser = serializers.TaskPlayerGetAdmin(instance=task_player,many=True).data
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = ser
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        '''添加管理员
            request:
                {
                    id:2 #任务ID
                    user_id_list: [1,2,3] # 用户id
                }
        '''
        ret = {}
        id = int(request.data['id'])
        user_id_list = request.data['user_id_list']
        task = models.Task.objects.get(id=id)
        for user_id in user_id_list:
            user = User.objects.get(id=user_id)
            models.TaskPlayer.objects.create(task=task,user=user,is_admin = True)
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)

    def delete(self, request, *args, **kwargs):
        '''删除管理员
            request:
                {
                    id:2 # 任务ID
                    user_id:3 # 用户ID
                }
        '''
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)


class TaskSwitch(APIView):

    def put(self, request, *args, **kwargs):
        '''修改任务状态
            request:
                id：任务ID
            response:
                true / false 修改后任务状态
        '''
        ret = {}
        id = request.data['id']
        flg = TaskManage().switch(id)
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = flg
        return JsonResponse(ret)

    def delete(self, request, *args, **kwargs):
        '''清除任务状态
            request:
                id:1 # 任务ID
        '''
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)


class Scheduling(APIView):
    def get(self, request, *args, **kwargs):
        '''获取班表
            request:
                id:1 # 任务id
            response:
                roster: 对应班表
        '''
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        '''更改班表
            request：
                roster: 对应班表
        '''
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)


class Condition(APIView):
    def get(self, request, *args, **kwargs):
        '''查看当天考勤工作情况
            request:
                id:2 # 任务id
            response:
                [
                    {
                        id:2 # 用户ID
                        name: 张三 
                    }
                ]
        权限判断
        '''
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)


class UndoRecord(APIView):

    def delete(self, request, *args, **kwargs):
        '''销假
            request：
               id:213 # 考勤记录id
        '''
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)


class OutData(APIView):
    def get(self, request, *args, **kwargs):
        '''导出今日记录情况
            request:
                id:任务ID
        '''
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)


class TaskExecutor(APIView):
    def get(self, request, *args, **kwargs):
        '''工作人员获取任务 
            response:
                [{
                    id:2                    # 任务ID
                    title:智慧彩云 晚查寝    # 名称
                    builder_name:张三       # 创建者姓名
                    is_finish:true          # 是否完成任务
                },]
        '''
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)


class Rule(APIView):
    def get(self, request, *args, **kwargs):
        '''获取规则
            request:
                codename: 规则编号
            response:
                list:[{
                    id:规则ID
                    title:规则名称
                    parent_id:父级ID
                }]
        '''
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
        return JsonResponse(ret)


class Submit(APIView):
    def post(self, request, *args, **kwargs):
        '''考勤提交
            request:
                id: 2               # 任务ID
                type: 0/1           # 提交类型 0=> 考勤提交 1=>执行人确认任务完成
                rule_id:[1,2,3]     # 规则的ID列表
                user_id:2           # 用户ID
                room_id:20          # 寝室ID
        '''
        ret = {'message': 'message', 'code': 2000, 'data': 'data'}
        return JsonResponse(ret)


class TaskRoomInfo(APIView):
    def get(self, request, *args, **kwargs):
        '''宿舍 相关任务信息
            request:
                task_id: 1 # 任务ID
                type: 
                    0 # 获取楼层
                    1 # 获取房间
                    2 # 获取房间内学生状态
        根据任务ID判断是查寝还是查卫生然后返回对应处理的数据
        '''
        ret = {'message': 'message', 'code': 2000, 'data': 'data'}
        return JsonResponse(ret)


class LateClass(APIView):
    API_PERMISSIONS = ['楼层号', 'get']

    def get(self, request, *args, **kwargs):
        '''晚自修 相关数据
            request:
                task_id:任务ID
                type: 
                    0 # 获取任务绑定的班级
                    1 # 获取班级名单附带学生多次点名情况
        '''
        ret = {}
        ret['message'] = 'message'
        ret['code'] = 2000
        ret['data'] = 'data'
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
