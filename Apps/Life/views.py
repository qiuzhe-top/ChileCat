"""
放置与寝室相关的活动
"""

from ..Life.utils import dormitory
from ..Life.utils.exceptions import *
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


class BuildingInfo(APIView):
    """获取楼号,包括层号"""

    API_PERMISSIONS = ['楼层号', 'get']

    def get(self, request):
        """获取楼号"""
        ret = {'code': 2000, 'message': "楼层遍历成功", 'data': dormitory.Room.building_info(request)}
        return JsonResponse(ret)


class RoomInfo(APIView):
    """
    获取房间信息
    需要参数:
        id,层号
    """

    API_PERMISSIONS = ['房间信息', 'get']

    def get(self, request):
        """获取房间信息"""
        ret = {
            'code': 0000,
            'message': "default message",
            'data': {}
        }
        req_list = self.request.query_params
        floor_id = req_list.get('floor_id', None)
        types = req_list.get('type', None)
        try:
            ret['data'] = dormitory.Room.room_info(floor_id,types)
            ret['code'] = 2000
            ret['message'] = "房间遍历成功"
        except RoomParamException as room_exception:
            ret['code'] = 4000
            ret['message'] = str(room_exception)
        return JsonResponse(ret)


class StudentPositionInfo(APIView):
    """
    学生位置(学生信息)
    需要前端给门号
        id
    """

    API_PERMISSIONS = ['寝室学生信息', 'get']

    def get(self, request):
        """拉取房间每个人的位置"""
        ret = {
            'code': 0000,
            'message': "default message",
            'data': []
        }
        req_list = self.request.query_params
        try:
            room_id = int(req_list.get('room_id', -1))
            types = req_list.get('type', None)
            if types == "floor-dorm":
                ret['data'] = dormitory.Room.student_info(room_id)
            else:
                ret['data'] = []
            ret['code'] = 2000
            ret['message'] = "房间读取成功"
        except ObjectDoesNotExist:
            ret['code'] = 4000
            ret['message'] = "房间或者房间内数据有误"
            ret['data'] = []
        except ValueError:
            ret['code'] = 4000
            ret['message'] = "参数错误"
        return JsonResponse(ret)


# class StudentLeak(APIView):
#     """
#     学生缺勤
#     前端提供:学生id,原因,房间id.
#     查寝人由系统自动查询当前登录用户
#     (是否归寝由这里系统自动改成0),
#     创建时间,最后修改时间由服务器自动生成
#     销假不在这里进行,故不设置
#     para: id,why,roomid
#     """
#
#     API_PERMISSIONS = ['学生缺勤', '*post']
#
#     def post(self, request):
#         """缺勤提交"""
#         ret = {
#             'code': 0000,
#             'message': "default message",
#         }
#         try:
#             dormitory_evening_check.DormitoryEveningCheck(
#                 self.request.query_params['act_id']).leak_submit(self.request.data)
#             ret['code'] = 2000
#             ret['message'] = "提交成功"
#         except ActivityException as e:
#             ret['code'] = 4000
#             ret['message'] = str(e)
#         except ActivityInitialization as e:
#             ret['code'] = 4000
#             ret['message'] = str(e)
#         return JsonResponse(ret)
#
#     def put(self, request):
#         """
#         销假
#         参数:请假条id,id
#         """
#         ret = {
#             'code': 0000,
#             'message': "default message",
#         }
#         dormitory_evening_check.DormitoryEveningCheck(self.request.query_params['act_id']).cancel()
#         ret['code'] = 2000
#         ret['message'] = "销假成功"
#         return JsonResponse(ret)
#
#
# class RecordSearch(APIView):
#     """记录查询返回所有缺勤记录"""
#     API_PERMISSIONS = ['缺勤公告', 'get']
#
#     def get(self, request):
#         """不给日期默认今天"""
#         search_date = self.request.data.get('date')
#         ret = {
#             'code': 2000, 'message': "查询成功",
#             'data': dormitory_evening_check.DormitoryEveningCheck.today_leaks(search_date)
#         }
#         return JsonResponse(ret)
#
#
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
