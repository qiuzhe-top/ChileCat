
'''
查寝api视图
'''
import json
import random
import math
import datetime
import xlrd
import xlwt
import os
import Apps.User
from io import BytesIO
from datetime import date
from Apps.Life import ser
from rest_framework.views import APIView
from django.utils.encoding import escape_uri_path
from django.http import JsonResponse,HttpResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from Apps.User.models import User
from .models import Building,Room,Manage,TaskRecord,StuInRoom,RoomHistory

class SwitchKnowing(APIView):
    '''全局开关,控制查寝活动能否进行'''
    def get(self,request):
        '''获取当前是否开启活动'''
        ret = {
            'code': 0000,
            'message': "default message",
            'data': ""
        }
        flag = Manage.objects.get(id=1).console
        ret['code'] = 2000
        ret['message'] = "状态获取成功"
        ret['data'] = flag
        return JsonResponse(ret)
    def post(self,request):
        '''开启活动'''
        ret = {
            'code': 0000,
            'message': "default message",
            'data': ""
        }
        flag = Manage.objects.get(id=1)
        if flag.console == "0":
            flag.console = "1"
        elif flag.console == "1":
            flag.console = "0"
        else:
            ret['code'] = 4000
            ret['message'] = "console不为1或者0,请去数据库检查"
        flag.save()
        ret['data'] = flag.console
        ret['code'] = 2000
        ret['message'] = "切换成功"
        return JsonResponse(ret)
    def put(self,request):
        '''初始化全部状态:房间状态,学生在寝室的状态'''
        ret = {
            'code': 0000,
            'message': "default message"
        }
        rooms = Room.objects.all()
        for room in rooms:
            room.status = "0"
            room.save()
        stus = StuInRoom.objects.all()
        for stu in stus:
            stu.status = "0"
            stu.save()
        ret['code'] = 2000
        ret['message'] = "状态重置成功"
        return JsonResponse(ret)

class Idcode(APIView):
    '''获取验证码'''
    def get(self,request):
        '''get'''
        ret = {
            'code': 0000,
            'message': "default message",
            'data': ""
        }
        flag = request.GET.get('flag',-1)
        today = date.today()
        if flag == -1:
            num = math.floor(1e5 * random.random())
            idcode = str(num)
            ret['data'] = idcode
            #获取今天时间
            manage_data = Manage.objects.filter(idcodetime=today)
            if manage_data.count() > 0:
                manage_data.first().idcode = idcode
            manage = Manage(1,today,idcode,"0")
            manage.save()
            ret['code'] = 2000
            ret['message'] = "获取验证码成功"
        else:
            idcode = Manage.objects.get(id=1)
            if idcode.idcodetime == today:
                ret['data'] = idcode.idcode
                ret['code'] = 2000
                ret['message'] = "获取验证码成功"
        return JsonResponse(ret)

    def post(self,request):
        '''验证验证码'''
        ret = {
            'code': 0000,
            'message': "default message"
        }
        reqlist = request.data
        req_idcode = reqlist.get('idcode',-1)
        if req_idcode == -1:
            ret['code'] = 4000
            ret['message'] = "参数错误,没有验证码信息"
            return JsonResponse(ret)
        today = date.today()
        manage_data = Manage.objects.filter(idcodetime=today)
        if manage_data.count() == 0:
            ret['code'] = 4000
            ret['message'] = "今日未发布验证码"
            return JsonResponse(ret)
        if manage_data.first().idcode == req_idcode:
            ret['code'] = 2000
            ret['message'] = "验证成功"
        else:
            ret['code'] = 4000
            ret['message'] = "验证失败"
        return JsonResponse(ret)

class Buildinginfo(APIView):
    '''获取楼号,包括层号'''
    def get(self,request):
        '''get'''
        ret = {
            'code': 0000,
            'message': "default message",
            'data': []
        }

        buildings = Building.objects.all()
        for i in buildings:
            #遍历每一栋楼
            building = {
                "id":"楼id",
                "name":"楼名称",
                "list":[]
            }
            building['id'] = i.id
            building['name'] = i.budnum + "号楼"
            floors = i.floor.all()
            for j in floors:
                #遍历每一层
                floor={
                    "id":"层id",
                    "name":"层名称",
                }
                floor['id'] = j.id
                floor['name'] = "第" + j.floornum + "层"
                building['list'].append(floor)
            ret['data'].append(building)
        ret['code'] = 2000
        ret['message'] = "楼层遍历成功"
        return JsonResponse(ret)

class Roominfo(APIView):
    '''
    获取房间信息
    需要参数:
        id,层号
    '''
    def get(self,request):
        '''get'''
        ret = {
            'code': 0000,
            'message': "default message",
            'data': {}
        }
        reqlist = request.GET
        try:
            floorid = int(reqlist.get('id',-1))
        except ValueError as id_lost:
            print(id_lost)
            ret['code'] = 4000
            ret['message'] = "缺少id"
            return JsonResponse(ret)
        if floorid == -1:
            ret['code'] = 4000
            ret['message'] = "缺少层号"
            return JsonResponse(ret)
        rooms = Room.objects.filter(floor_id=floorid)
        if rooms.count() == 0:
            ret['code'] = 4000
            ret['message'] = "房间数为空"
            return JsonResponse(ret)
        roomlist = []
        for i in rooms:

            room = {
                "id":"房间id",
                "name":"房间名称",
                "status":"状态(是否被查)"
            }
            room['id'] = i.id
            room['name'] = i.roomnum
            room['status'] = i.status
            roomlist.append(room)
        ret['data'] = roomlist
        ret['code'] = 2000
        ret['message'] = "房间遍历成功"
        return JsonResponse(ret)

class Stupositioninfo(APIView):
    '''
    学生位置(学生信息)
    需要前端给门号
        id
    '''
    def get(self,request):
        '''拉取房间每个人的位置'''
        ret = {
            'code': 0000,
            'message': "default message",
            'data': []
        }
        req_list = request.GET
        try:
            roomid = int(req_list.get('id',-1))
            if roomid == -1:
                ret['code'] = 4000
                ret['message'] = "参数错误"
                return JsonResponse(ret)
            room = Room.objects.get(id=roomid)
            room_data = room.stuinroom.all()
            for i in room_data:
                unit = {
                    "id":"学生id",
                    "name":"学生名称",
                    "status":"学生状态",
                    "position":"床位"
                }
                unit['id'] = i.stuid.id
                unit['name'] = i.stuid.userinfo.name
                unit['status'] = i.status
                unit['position'] = i.bedposition
                ret['data'].append(unit)
            ret['code'] = 2000
            ret['message'] = "房间读取成功"
        except ObjectDoesNotExist as room_not_find:
            print("房间或者用户有误 ",room_not_find)
            ret['code'] = 4000
            ret['message'] = "房间或者房间内数据有误"
            ret['data'] = []
            return JsonResponse(ret)
        except ValueError as id_not_number:
            print("参数错误 ",id_not_number)
            ret['code'] = 4000
            ret['message'] = "参数错误"
            return JsonResponse(ret)
        return JsonResponse(ret)

class Studentleak(APIView):
    '''
    学生缺勤
    前端提供:学生id,原因,房间id.
    查寝人由系统自动查询当前登录用户
    (是否归寝由这里系统自动改成0),
    创建时间,最后修改时间由服务器自动生成
    销假不在这里进行,故不设置
    para: id,why,roomid
    '''
    def post(self,request):
        '''缺勤提交'''
        ret = {
            'code': 0000,
            'message': "default message",
        }
        print(Manage.objects.get(id=1).console)
        if Manage.objects.get(id=1).console == "0":
            ret['code'] = 4000
            ret['message'] = "任务未开始!"
            return JsonResponse(ret)
        req_list = request.data
        stuleaks = req_list.get('datas',[])
        try:
            worker = User.utils.auth.get_user(request)
            room = Room.objects.get(id = int(req_list.get('roomid',"")))
            hisrecords = TaskRecord.objects.filter(
                Q(createdtime__date=datetime.date.today())&Q(roomid=room)
            )
            if stuleaks != []:
                for i in stuleaks:
                    stuid = i.get('id',-1)
                    if stuid == -1:
                        ret['code'] = 4000
                        ret['message'] = "内部数据错误"
                        break
                    stuid = User.models.User.objects.get(id=int(stuid))
                    reason = i.get('why',"")
                    status = i.get('status',"1")
                    stu = StuInRoom.objects.get(stuid=stuid)
                    stu.status = status
                    #原来已有的记录删除,新建,更新
                    oldrecords = TaskRecord.objects.filter(
                        Q(createdtime__date=datetime.date.today())&
                        Q(objstuid=stuid)
                        )
                    if oldrecords:
                        for j in oldrecords:
                            j.delete()
                    stu.save()
                    if worker == -1:
                        ret['code'] = 4000
                        ret['message'] = "执行人信息有误"
                        return JsonResponse(ret)
                    budid = room.floor.budid
                    last_time = datetime.datetime.now()
                    record = TaskRecord(
                        workerid=worker,
                        objstuid=stuid,
                        reason=reason,
                        flag=status,
                        lastmodifytime=last_time,
                        buildingid=budid,
                        roomid=room
                        )
                    record.save()
            #修改房间状态(被查)
            room.status = "1"
            #print("准备保存")
            room.save()
            #print("保存成功")
            #创建查房记录
            roomhistory = RoomHistory(
                roomid=room,managerid=worker,
                createdtime=datetime.datetime.now()
                )
            roomhistory.save()
            ret['code'] = 2000
            ret['message'] = "提交成功"
        except AttributeError as str_not_get:
            print(str_not_get)
            ret['code'] = 4000
            ret['message'] = "房间号有误"
        except ObjectDoesNotExist as para_lost:
            print(para_lost)
            ret['code'] = 4000
            ret['message'] = "学生不存在"
        finally:
            return JsonResponse(ret)
    def put(self,request):
        '''
        销假
        参数:请假条id,id
        '''
        ret = {
            'code': 0000,
            'message': "default message",
        }
        req_list = request.data
        try:
            data_id = req_list['id']
            req_flag = req_list.get('flag',"是")
            data = TaskRecord.objects.get(id=int(data_id))
            data.flag = req_flag
            data.save()
            ret['code'] = 2000
            ret['message'] = "销假成功"
        except ObjectDoesNotExist as data_lost:
            print("记录不存在")
            ret['code'] = 4000
            ret['message'] = "记录不存在"
        except KeyError as key_lost:
            ret['code'] = 4000
            ret['message'] = "参数缺失"
        finally:
            return JsonResponse(ret)

class Recordsearch(APIView):
    '''记录查询返回所有缺勤记录'''
    def get(self,request):
        '''get'''
        today = date.today()
        ret = {
            'code': 0000,
            'message': "default message",
            'data': ""
        }
        data = TaskRecord.objects.filter(Q(flag="1")&Q(createdtime__date=today))
        print(data)
        serdata = ser.TaskTecordSerializer(instance=data,many=True).data
        ret['code'] = 2000
        ret['message'] = "查询成功"
        ret['data'] = serdata
        return JsonResponse(ret)

class ExportExcel(APIView):
    '''导出excel'''
    def get(self,request):
        '''给日期,导出对应的记录的excel表,不给代表今天'''
        response = HttpResponse(content_type='application/vnd.ms-excel')
        filename = datetime.date.today().strftime("%Y-%m-%d")  + ' 学生缺勤表.xls'
        response['Content-Disposition'] = (
            'attachment; filename={}'.format(escape_uri_path(filename))
            )
        req_list = request.GET
        time = req_list.get('date',-1)
        if time == -1:
            time = date.today()
        records = TaskRecord.objects.filter(Q(flag="1")&Q(createdtime__date=time))
        if not records:
            return HttpResponse(
                json.dumps({"state": "1", "msg": "查无数据,导出失败"}), content_type="application/json"
                )
        serrecords = ser.TaskTecordSerializer1(instance=records,many=True).data
        if serrecords:
            ws = xlwt.Workbook(encoding='utf-8')
            w = ws.add_sheet('sheet1')
            w.write(0,0,u'日期')
            w.write(0,1,u'楼号')
            w.write(0,2,u'班级')
            w.write(0,3,u'学号')
            w.write(0,4,u'姓名')
            w.write(0,5,u'原因')
            row = 1
            for i in serrecords:
                k = dict(i)
                column = 0
                for j in k.values():
                    w.write(row,column,j)
                    column += 1
                row += 1
            #循环完成
            path = os.getcwd()
            ws.save(path+"/leaksfile/{}".format(filename))
            output = BytesIO()
            ws.save(output)
            output.seek(0)
            response.write(output.getvalue())
        return response
