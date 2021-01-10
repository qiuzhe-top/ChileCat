
'''
查寝api视图
'''
import random
import math
import datetime
import User
from life import ser
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import Building,Room,Manage,TaskRecord,StuInRoom



class Idcode(APIView):
    '''获取验证码'''
    def get(self,request):
        '''get'''
        ret = {
            'code': 0000,
            'message': "default message",
            'data': ""
        }
        num = math.floor(1e5 * random.random())
        idcode = str(num)
        ret['data'] = idcode
        #获取今天时间
        today = datetime.datetime.today()
        manage_data = Manage.objects.filter(idcodetime=today)
        if manage_data.count() > 0:
            manage_data.first().idcode = idcode
        manage = Manage(1,today,idcode,"0")
        manage.save()
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
        today = datetime.datetime.today()
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
        floorid = reqlist.get('id',-1)
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
    学生位置
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
                    "position":"床位"
                }
                unit['id'] = i.stuid.id
                unit['name'] = i.stuid.userinfo.name
                unit['position'] = i.bedposition
                ret['data'].append(unit)
            ret['code'] = 2000
            ret['message'] = "房间读取成功"
        except ObjectDoesNotExist as room_not_find:
            print("房间不存在 ",room_not_find)
            ret['code'] = 4000
            ret['message'] = "房间不存在 " + room_not_find
            return JsonResponse(ret)
        except ValueError as id_not_number:
            print("参数错误 ",id_not_number)
            ret['code'] = 4000
            ret['message'] = "参数错误 " + id_not_number
            return JsonResponse(ret)
        return JsonResponse(ret)

class Studentleak(APIView):
    '''
    学生缺勤
    前端提供,查寝人id,学生id,原因,楼id,销假人id在此为空、不写
    (是否归寝由这里系统自动改成0),创建时间,最后修改时间由服务器自动生成
    para: workid,stuid,reason,budid.
    '''
    def post(self,request):
        '''post'''
        ret = {
            'code': 0000,
            'message': "default message",
        }
        req_list = request.data
        workerid = req_list.get('workid',-1)
        stuid = req_list.get('stuid',-1)
        reason = req_list.get('reason',-1)
        print(workerid,stuid,reason)
        if workerid == -1 or stuid == -1 or reason == -1:
            print("参数不完整")
            ret['code'] = 4000
            ret['message'] = "参数缺失"
            return JsonResponse(ret)
        try:
            workerid = User.models.User.objects.get(id = int(workerid))
            stuid = User.models.User.objects.get(id = int(stuid))
            roomid = StuInRoom.objects.get(stuid=stuid).roomid
            budid = roomid.floor.budid
            last_time = datetime.datetime.now()
            record = TaskRecord(
                workerid=workerid,
                objstuid=stuid,
                reason=reason,
                flag="0",
                lastmodifytime=last_time,
                buildingid=budid,
                roomid=roomid
                )
            record.save()
            ret['code'] = 2000
            ret['message'] = "学生: " + stuid.userinfo.name + " 缺勤执行完成"
        except ObjectDoesNotExist as para_leak:
            print("参数错误",para_leak)
            ret['code'] = 4000
            ret['message'] = "参数错误(错误的楼号/执行者/被执行者)"
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
        data_id = request.data.get(id)
        try:
            data = TaskRecord.objects.get(id=id)
            data.flag = "1"
            data.save()
            ret['code'] = 2000
            ret['message'] = "销假成功"
        except ObjectDoesNotExist as data_lost:
            print("记录不存在")
            ret['code'] = 4000
            ret['message'] = "记录不存在"
        finally:
            return JsonResponse(ret)

class Recordsearch(APIView):
    '''记录查询返回所有缺勤记录'''
    def get(self,request):
        '''get'''
        ret = {
            'code': 0000,
            'message': "default message",
            'data': ""
        }
        data = TaskRecord.objects.filter(flag="0")
        serdata = ser.TaskTecordSerializer(instance=data,many=True).data
        ret['code'] = 2000
        ret['message'] = "查询成功"
        ret['data'] = serdata
        return JsonResponse(ret)
