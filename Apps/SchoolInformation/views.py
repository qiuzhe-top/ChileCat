import json
import re
from Apps.User.models import StudentInfo, UserInfo
from Apps.SchoolAttendance import models
import os
import time
from django.contrib.auth.models import User
from django.core.checks import messages
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from openpyxl.reader.excel import load_workbook

# Create your views here.


class StudentInformation(APIView):
    API_PERMISSIONS = ['考勤搜索用户信息', '*get']

    def get(self, request, *args, **kwargs):
        '''
          request:
            username: 19510146 # 学号
          response:
            {
              id:1 # 学生ID
              name: 张三 # 学生姓名
              phone: 19101245412 #电话
            }
        '''
        # TODO 添加搜索多个用户
        ret = {}
        try:
            username = request.GET['username']
            user = User.objects.get(username=username)
            ret['data'] ={
                "username":username,
                "name":user.userinfo.name,
                "tel":user.userinfo.tel,
                "grade":user.studentinfo.grade.name
            }
            ret['message'] = '搜索成功'
            ret['code'] = 2000
            return JsonResponse(ret)
        except:
            ret['code'] = 4000
            ret['message'] = '没有用户'+username+'或用户信息不完整'
        return JsonResponse(ret)



class AddUser(APIView):

    def post(self,request, *args, **kwargs):
        type_ = request.data['type']
        if type_ == '0':
          ret = update_or_create_user(request)
        elif type_ == '1':
          ret = update_or_create_stu_in_room(request)
        return JsonResponse(ret)

# 添加学生
def update_or_create_user(request):

    file = request.data['file']
    # from openpyxl.reader.excel import load_workbook
    wb = load_workbook(file,read_only=True)

    error_list=[] # 执行中错误记录
    grade_dict = {} # 班级对象

    for rows in wb:
        for row in rows: #遍历行
          
            try:
                username = row[0].internal_value # 学号
            except Exception  as e:
                print(e)
                continue
                
            if not username:
                continue

            username = re.findall('[a-zA-Z0-9]+',str(username),re.S)[0]
            name = row[ 1].internal_value # 姓名
            name = re.findall('[\u4e00-\u9fa5]+',str(name),re.S)[0]
            grade_ = row[2].internal_value # 班级
            grade = re.findall('[a-zA-Z0-9]+',str(grade_),re.S)[0]

            # 获取用户
            u = User.objects.filter(username = username)

            if len(u)==0:
                u = User.objects.create_user(username=username,password=username)
            else:
                u = u[0]

            # 修改用户姓名
            user_info,flg = UserInfo.objects.get_or_create(user=u)
            user_info.name = name
            user_info.save()

            # 获取班级
            is_grade = grade_dict.get(grade,False)
            if is_grade:
              grade = grade_dict[grade]
            else:
              grade = models.Grade.objects.filter(name=grade)
              if len(grade)==1:
                grade = grade[0]
                grade_dict[grade] = grade
                # 绑定班级
                stu_info,flg = StudentInfo.objects.get_or_create(user=u,defaults={'grade':grade})
                if not flg:
                  stu_info.grade = grade
                  stu_info.save()
              else:
                error_list.append({
                    'username':username,
                    'name':name,
                    'grade':grade_,
                    'messages':'用户更新正常 班级不存在 所以未绑定'
                })
                grade = False
    ret = {}
    ret['code'] = 2000
    ret['data'] = error_list
    return ret

# 学生寝室更新
def update_or_create_stu_in_room(request):

    file = request.data['file']
    wb = load_workbook(file,read_only=True)

    error_list=[] # 执行中错误记录

    for rows in wb:
        for row in rows: #遍历行

            try:
                username = row[0].internal_value # 学号
            except Exception  as e:
                continue
                
            if not username:
                continue

            username = re.findall('[a-zA-Z0-9]+',str(username),re.S)[0]

            room_ = row[1].internal_value # 寝室编号
            room = re.findall('[a-zA-Z0-9#]+',str(room_),re.S)[0]
          
            # 获取用户
            try:
                u = User.objects.get(username = username)
            except:
                error_list.append({
                  'username':username,
                  'message':'用户不在系统内'
                })
                continue
            
            # 如果寝室号为空就删除当前用户对应的寝室信息
            if room_ == None:
              models.StuInRoom.objects.filter(student = u).delete()
              continue
            
            # 解析寝室字符串
            room_str = room.split('#')
            building = room_str[0]
            floor = room_str[1][:1]
            room = room_str[1][1:]

            # 找到对应的寝室房间
            bu,flg = models.Building.objects.get_or_create(name=building)
            fl,flg = models.Floor.objects.get_or_create(building=bu,name=floor)
            room,flg = models.Room.objects.get_or_create(floor=fl,name=room)

            try:
              models.StuInRoom.objects.filter(student = u).delete()
              models.StuInRoom.objects.create(student = u,room=room)
            except:
              error_list.append({
                  'username':username,
                  'message':'房间绑定失败'
                })
                
    ret = {}
    ret['code'] = 2000
    ret['data'] = error_list
    return ret
