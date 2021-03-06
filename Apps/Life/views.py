"""
查寝api视图
"""
import json
import datetime
import xlwt
import os
from io import BytesIO
from datetime import date
from Apps.Life import ser
from Apps.Life.utils import dormitory, activities, leak
from Apps.Life.utils.exceptions import *
from rest_framework.views import APIView
from django.utils.encoding import escape_uri_path
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import TaskRecord
from django.contrib.auth.models import AnonymousUser, User


class SwitchKnowing(APIView):
    """全局开关,控制查寝活动能否进行"""
    auth = {
        'name': ("api-control_life_activity", "api-活动控制"),
        'method': {'GET', 'POST', 'PUT'}
    }

    activity = activities.ActivityControl()

    def get(self, request):
        """获取当前是否开启活动"""
        ret = {
            'code': 0000,
            'message': "default message",
            'data': ""
        }

        flag = self.activity.get_status()
        ret['code'] = 2000
        ret['message'] = "状态获取成功"
        ret['data'] = flag
        return JsonResponse(ret)

    def post(self, request):
        """切换活动状态(开/关)"""
        ret = {'code': 2000, 'message': "切换成功", 'data': self.activity.switch()}
        return JsonResponse(ret)

    def put(self, request):
        """初始化全部状态:房间状态,学生在寝室的状态"""
        ret = {
            'code': 0000,
            'message': "default message"
        }
        self.activity.initialization()
        ret['code'] = 2000
        ret['message'] = "状态重置成功"
        return JsonResponse(ret)


class VerificationCode(APIView):
    """获取验证码 url:/api/life/idcode"""
    auth = {
        'name': ("api-verification_code", "api-验证码相关"),
        'method': {'GET', 'POST', 'PUT'}
    }
    activity = activities.ActivityControl()

    def get(self, request):
        """获取"""
        ret = {'code': 0000, 'message': "default message", 'data': None}
        try:
            ret['data'] = self.activity.get_verification_code()
            ret['code'] = 2000
            ret['message'] = "获取成功"
        except TimeVerificationCodeException as act_error:
            ret['code'] = 4000
            ret['message'] = str(act_error)
        return JsonResponse(ret)

    def put(self, request):
        """生成验证码"""
        ret = {'code': 2000, 'message': "生成验证码成功", 'data': self.activity.generate_verification_code()[0]}
        return JsonResponse(ret)

    def post(self, request):
        """验证验证码"""
        ret = {
            'code': 0000,
            'message': "default message"
        }
        req_list = self.request.data
        req_id_code = req_list.get('idcode', -1)
        try:
            self.activity.verify(req_id_code)
            ret['code'] = 2000
            ret['message'] = "验证成功"
        except VerificationCodeException as code_error:
            ret['code'] = 4000
            ret['message'] = str(code_error)
        return JsonResponse(ret)


class BuildingInfo(APIView):
    """获取楼号,包括层号"""
    auth = {
        'name': ("api-building_info", "api-获取楼层号"),
        'method': {'GET'}
    }

    @staticmethod
    def get(request):
        """获取楼号"""
        ret = {'code': 2000, 'message': "楼层遍历成功", 'data': dormitory.Room.building_info()}
        return JsonResponse(ret)


class RoomInfo(APIView):
    """
    获取房间信息
    需要参数:
        id,层号
    """
    auth = {
        'name': ("api-room_info", "api-获取房间信息"),
        'method': {'GET'}
    }

    def get(self, request):
        """获取房间信息"""
        ret = {
            'code': 0000,
            'message': "default message",
            'data': {}
        }
        req_list = self.request.query_params
        floor_id = req_list.get('floor_id', None)
        try:
            ret['data'] = dormitory.Room.room_info(floor_id)
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
    auth = {
        'name': ("api-student_position", "api-获取学生位置"),
        'method': {'GET'}
    }

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
            ret['data'] = dormitory.Room.student_info(room_id)
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
    auth = {
        'name': ("api-student_leak", "api-缺勤,销假相关"),
        'method': {'POST', 'PUT'}
    }

    def post(self, request):
        """缺勤提交"""
        ret = {
            'code': 0000,
            'message': "default message",
        }
        print(self.request.user)
        if self.request.user == AnonymousUser:
            ret['code'] = 5500
            ret['message'] = "用户异常"
            return JsonResponse(ret)
        try:
            leak.Leak(self.request).submit()
            ret['code'] = 2000
            ret['message'] = "提交成功"
        except TimeActivityException as activity_error:
            ret['code'] = 4000
            ret['message'] = str(activity_error)
        except VerificationCodeException as act_error:
            ret['code'] = 4000
            ret['message'] = str(act_error)
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
        leak.Leak(self.request).cancel()
        ret['code'] = 2000
        ret['message'] = "销假成功"
        return JsonResponse(ret)


class RecordSearch(APIView):
    API_PERMISSIONS = ['缺勤公告','get']
    
    """记录查询返回所有缺勤记录"""
    auth = {
        'name': ("api-leaks_search", "api-缺勤查询"),
        'method': {'POST'}
    }

    def get(self, request):
        """不给日期默认今天"""
        search_date = self.request.data.get('date')
        ret = {'code': 2000, 'message': "查询成功", 'data': leak.Leak.today_leaks(search_date)}
        return JsonResponse(ret)


class ExportExcel(APIView):
    """导出excel """
    auth = {
        'name': ("api-export_excel", "api-缺勤导出excel"),
        'method': {'GET'}
    }

    def get(self, request):
        """给日期,导出对应的记录的excel表,不给代表今天"""
        print("准备导出excel")
        response = HttpResponse(content_type='application/vnd.ms-excel')
        filename = datetime.date.today().strftime("%Y-%m-%d") + ' 学生缺勤表.xls'
        response['Content-Disposition'] = (
            'attachment; filename={}'.format(escape_uri_path(filename))
        )
        req_list = self.request.query_params
        time = req_list.get('date', -1)
        if time == -1:
            time = date.today()
        records = TaskRecord.objects.filter(Q(flag="0") & Q(created_time__date=time))
        if not records:
            return JsonResponse(
                {"state": "1", "msg": "无数据,导出失败"}
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
            path = os.getcwd()
            # ws.save(path + "/leaksfile/{}".format(filename))
            output = BytesIO()
            ws.save(output)
            output.seek(0)
            response.write(output.getvalue())
            print("导出excel")
        return response
