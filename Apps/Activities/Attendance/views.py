import datetime
# import os
import xlwt
from io import BytesIO
from datetime import date
from ..Attendance.Entity import ser
from rest_framework.views import APIView
from django.utils.encoding import escape_uri_path
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from Apps.Activity.models import TaskRecord
from ..Attendance.Entity import dormitory_evening_check
from Apps.Activity.utils.activity_factory import ActivityFactory
from Apps.Activity.utils.exceptions import *


# Create your views here.


class StudentLeak(APIView):
    """
    学生缺勤
    前端提供:学生id,原因,房间id.
    查寝人由系统自动查询当前登录用户
    (是否归寝由这里系统自动改成0),
    创建时间,最后修改时间由服务器自动生成
    销假不在这里进行,故不设置
    para: id,why,roomid
    """

    API_PERMISSIONS = ['学生缺勤', '*post']

    def post(self, request):
        """缺勤提交"""
        ret = {
            'code': 0000,
            'message': "default message",
        }
        print(self.request.data)
        try:
            ActivityFactory(
                self.request.query_params['act_id']).leak_submit(self.request.data)
            ret['code'] = 2000
            ret['message'] = "提交成功"
        except ActivityException as e:
            ret['code'] = 4000
            ret['message'] = str(e)
        except ActivityInitialization as e:
            ret['code'] = 4000
            ret['message'] = str(e)
        return JsonResponse(ret)

    def put(self, request):
        """
        销假
        参数:请假条id,id
        """
        ret = {
            'code': 0000,
            'message': "default message",
        }
        try:
            ActivityFactory(
                manage_id=self.request.query_params['act_id']
            ).cancel(self.request.data['task_id'], self.request.user)
            ret['code'] = 2000
            ret['message'] = "销假成功"
        except DormitoryEveningCheckException as e:
            ret['code'] = 4000
            ret['message'] = str(e)
        return JsonResponse(ret)


class RecordSearch(APIView):
    """记录查询返回所有缺勤记录"""
    API_PERMISSIONS = ['缺勤公告', 'get']

    def get(self, request):
        """不给日期默认今天"""
        search_date = self.request.data.get('date')
        if not search_date:
            search_date = datetime.date.today()
        ret = {
            'code': 2000, 'message': "查询成功",
            'data': ActivityFactory.today_leaks(search_date)
        }
        return JsonResponse(ret)


class ExportExcel(APIView):
    """导出excel """

    API_PERMISSIONS = ['查寝Excel记录', 'get']

    def get(self, request):
        """给日期,导出对应的记录的excel表,不给代表今天"""
        print("准备导出excel")
        response = HttpResponse(content_type='application/vnd.ms-excel')
        filename = datetime.date.today().strftime("%Y-%m-%d") + ' 学生缺勤表.xls'
        response['Content-Disposition'] = (
            'attachment; filename={}'.format(escape_uri_path(filename))
        )
        req_list = self.request.query_params
        time_get = req_list.get('date', -1)
        if time_get == -1:
            time_get = date.today()
        records = TaskRecord.objects.filter(Q(task_type__types="dorm") & Q(manager=None) & Q(created_time__date=time_get))
        if not records:
            return JsonResponse(
                {"state": "1", "msg": "当日无缺勤"}
            )
        ser_records = ser.TaskRecordExcelSerializer(instance=records, many=True).data
        if ser_records:
            ws = xlwt.Workbook(encoding='utf-8')
            w = ws.add_sheet('sheet1')
            w.write(0, 0, u'日期')
            w.write(0, 1, u'楼号')
            w.write(0, 2, u'班级')
            w.write(0, 3, u'学号')
            w.write(0, 4, u'姓名')
            w.write(0, 5, u'原因')
            row = 1
            for i in ser_records:
                k = dict(i)
                column = 0
                for j in k.values():
                    w.write(row, column, j)
                    column += 1
                row += 1
            # 循环完成
            # path = os.getcwd()
            # ws.save(path + "/leaksfile/{}".format(filename))
            output = BytesIO()
            ws.save(output)
            output.seek(0)
            response.write(output.getvalue())
            print("导出excel")
        return response
