import datetime
# import os
# import xlwt
# from io import BytesIO
# from datetime import date
# from django.utils.encoding import escape_uri_path
# from django.db.models import Q
# from Apps.Activity.models import TaskRecord
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from Apps.Activity.utils.activity_factory import ActivityFactory
from Apps.Activities.Attendance.Entity import dormitory_evening_check
from .utils.exceptions import *
from .models import *
from .ser import ManageSerializer


# Create your views here.


class SwitchKnowing(APIView):
    """控制活动"""
    API_PERMISSIONS = ['活动开关', 'get']

    def get(self, request):
        """获取当前是否开启活动"""
        ret = {
            'code': 0000,
            'message': "default message",
            'data': ""
        }
        flag = ActivityFactory(self.request.query_params['act_id']).get_status()
        # flag = AttendanceActivityControl(self.request.query_params['act_id']).get_status()
        ret['code'] = 2000
        ret['message'] = "状态获取成功"
        ret['data'] = flag
        return JsonResponse(ret)

    def post(self, request):
        """切换活动状态(开/关)"""
        ret = {
            'code': 2000, 'message': "切换成功",
            'data': ActivityFactory(self.request.query_params['act_id']).switch()
            # 'data': AttendanceActivityControl(self.request.query_params['act_id']).switch()
        }
        return JsonResponse(ret)

    def put(self, request):
        """初始化活动,怎么初始化由底层决定"""
        ret = {
            'code': 0000,
            'message': "default message"
        }
        try:
            ActivityFactory(self.request.query_params['act_id']).initialization()
            ret['code'] = 2000
            ret['message'] = "状态重置成功"
        except DormitoryEveningCheckException as e:
            ret['code'] = 4000
            ret['message'] = str(e)
        return JsonResponse(ret)


class VerificationCode(APIView):
    """获取能开什么活动"""

    API_PERMISSIONS = ['工作验证码', 'get', 'post']

    def get(self, request):
        """能开什么活动"""
        ret = {'code': 4000, 'message': "default", 'data': ''}
        role = self.request.query_params['role']
        pers = self.request.user.get_all_permissions()
        perms = []
        if role == "activity_admin":
            for per in pers:
                if "Activity.attendance-" in per and per[-5:] == "admin":
                    perms.append(str(per).split('.')[1])
            act_list = Manage.objects.filter(code_name__in=perms)
            ret['data'] = ManageSerializer(instance=act_list, many=True).data
            ret['code'] = 2000
            ret['message'] = "管理员获取"
        elif role == "attendance_worker":
            for per in pers:
                if "Activity.attendance-" in per and per[-5:] != "admin":
                    perms.append(str(per).split('.')[1])
            act_list = Manage.objects.filter(code_name__in=perms)
            ret['data'] = ManageSerializer(instance=act_list, many=True).data
            ret['code'] = 2000
            ret['message'] = "工作人员获取"
        return JsonResponse(ret)

    def put(self, request):
        """生成验证码"""
        ret = {
            'code': 2000, 'message': "生成验证码成功",
            'data': ActivityFactory(self.request.query_params['act_id']).generate_verification_code()
        }
        return JsonResponse(ret)

    def post(self, request):
        """验证验证码"""
        ret = {
            'code': 0000,
            'message': "default message"
        }
        req_list = self.request.data
        req_id_code = req_list.get('idcode', -1)
        if ActivityFactory(self.request.query_params['act_id']).verify(req_id_code):
            ret['code'] = 2000
            ret['message'] = "验证成功"
        else:
            ret['code'] = 4000
            ret['message'] = "验证失败"
        return JsonResponse(ret)

# class ExportExcel(APIView):
#     """导出excel """
#
#     API_PERMISSIONS = ['查寝Excel记录', 'get']
#
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
#         records = TaskRecord.objects.filter(Q(manager=None) & Q(created_time__date=time_get))
#         if not records:
#             return JsonResponse(
#                 {"state": "1", "msg": "当日无缺勤"}
#             )
#         ser_records = ser.TaskRecordExcelSerializer(instance=records, many=True).data
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
#         return response
