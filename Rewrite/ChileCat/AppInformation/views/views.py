'''
Author: 邹洋
Date: 2022-02-07 13:57:05
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 17:48:46
Description: 
'''
from cool.views import CoolAPIException, ErrorCode, ViewSite
from django.http import JsonResponse
from AppInformation import models
from AppInformation.common.launch import run_init
from AppInformation.models import College
from AppUser.common.configuration import PASSWOED_123456
from Core.common.excel import ExcelBase
from .dormitory import urlpatterns_dormitory
from Core.views import PermissionView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import fields
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, utils

from AppInformation import serializers

User = get_user_model()
site = ViewSite(name='AppInformation', app_name='AppInformation')


 
@site
class StudentInformation(PermissionView):

    name = _('考勤 获取用户基本信息')
    response_info_serializer_class = serializers.UserSerializer

    def get_context(self, request, *args, **kwargs):
        username = request.params.username
        user = User.objects.filter(username=username)
        if not user.exists():
            raise CoolAPIException(ErrorCode.ERR_USER_UNABLE_TO_SEARCH_FOR_USERR)
        return serializers.UserSerializer(user[0], request=request).data

    class Meta:
        param_fields = (
            ('username', fields.CharField(label=_('用户名'), max_length=25)),
        )

@site
class CollegeQuery(PermissionView):
    name = _('获取分院')
    
    def get_context(self, request, *args, **kwargs):
        d =  College.objects.all().values('id','name')
        return list(d)



# ================================================= #
# ************** 系统管理员          ************** #
# ================================================= #
@site
class UploadUserInformation(PermissionView, ExcelBase):
    name = _('用户信息上传')

    def add_message(self,*d):
        self.message.append(d)
    def check_room_str(self,room):
        # 房间字符串(3#102)格式检查
        if len(room) != 5:
            return False
        if room[1] != '#':
            return False
        return True
    def get_context(self, request, *args, **kwargs):
        rows = self.excel_to_list(request)
        self.message = []

        # 去重后的学生学号、姓名列表
        username_simple_dict = {}
        # 学号列表
        usernames = username_simple_dict.keys()
        # 学号和学生信息字典
        username_dict = {}
        # 班级列表
        grade_set = set()
        # 房间列表
        room_set = set()
        # 分院
        college_id = rows[0]['college']
        # 字段检查
        ks = rows[0].keys()
        check_username = 'username' in ks
        check_room = 'room' in ks
        check_grade = 'grade' in ks
        check_name = 'name' in ks
        check_college = 'college' in ks
        if not check_username:
            return ['缺少学号']
        if not check_college:
            return ['缺少分院']

        # 根据学号标记重复
        for row in rows:
            username = row['username']
            username_dict[username] = {'repeat_number':0,'data':row}

        for row in rows:
            username = row['username']
            username_dict[username]['repeat_number'] += 1
        
        for row in rows:
            username = row['username']
            check_n = username_dict[username]['repeat_number'] == 1
            if check_n:
                # 添加班级
                if check_grade:
                    grade_set.add(row['grade'])
                # 添加房间
                if check_room:
                    room = row['room']
                    if self.check_room_str(room):
                        room_set.add(room)
                    else:
                        self.add_message(username,room,'班级编号格式不正确')
                # 添加姓名
                if check_name:
                    # username_list.append([username,row['name']])
                    username_simple_dict[username] = row['name']
            else:
                self.add_message(username,'学号重复')
        if check_grade:
            # 创建班级
            db_grade = models.Grade.objects.filter(id__in=list(grade_set)).values_list('id',flat=True)
            models_grade = []
            for grade in grade_set - set(db_grade):
                models_grade.append(models.Grade(id=grade,college_id=college_id))
            models.Grade.objects.bulk_create(models_grade)

        if check_username:
            # 创建用户
            mode_users = []
            usernames = list(username_simple_dict.keys())
            db_usernames = User.objects.all().values_list('username',flat=True)
            # 循环数据库没有的账号
            for username in set(usernames) - set(db_usernames):
                name = username_simple_dict[username]
                grade = username_dict[username]['data']['grade']
                value = {"username":username,"name":name,"password":PASSWOED_123456}
                if check_grade:
                    value['grade_id'] = grade
                mode_users.append(User(**value))
            User.objects.bulk_create(mode_users)
        user_all = User.objects.all().values_list('username','id')
        db_user_id = {}
        


        for user in  user_all:
            db_user_id[user[0]] = user[1]

        if check_room:
            # 创建房间
            db_room_set = set(models.DormitoryBuilding.objects.filter(id__in=list(room_set)).values_list('id',flat=True))
            models_room = []
            for room in room_set - db_room_set:
                models_room.append(models.DormitoryBuilding(id=room))
            models.DormitoryBuilding.objects.bulk_create(models_room)
            # 学生和房间绑定
            db_usernames = models.StuInRoom.objects.all().values_list('user__username',flat=True)
            models_stu_in_room = []
            for username in set(usernames) - set(db_usernames):
                obj = username_dict[username]['data']
                user_id = db_user_id[username]
                value = {"room_id":obj["room"],"user_id":user_id}
                models_stu_in_room.append(models.StuInRoom(**value))
            models.StuInRoom.objects.bulk_create(models_stu_in_room)


        return self.message
    class Meta:
        param_fields = (
            ('username', fields.CharField(label=_('用户名'), default=None)),
        )
@site
class BuildingManagr(CoolBFFAPIView):
    name = _('宿舍楼数据管理')

    def filter_building_all(self,request):
        # 查询全部
        data = models.DormitoryBuilding.objects.all().order_by('id').values_list('id',flat=True)
        print(list(data))
        return list(data)
        
    def filter_stu_room_all(self,request):
        # 查询全部
        data = models.StuInRoom.objects.all().values('id','room','username','bed_position')
        return list(data)

    def filter_by_building_in_list(self,request):
        q = request.params.building_list
        data = models.DormitoryBuilding.objects.filter(building__in = q).values('id')
        return list(data)

    def get_context(self, request, *args, **kwargs):
        fun = {}
        fun['filter_building_all'] = self.filter_building_all
        fun['filter_stu_room_all'] = self.filter_stu_room_all
        fun['filter_by_building_in_list'] = self.filter_by_building_in_list
        return fun[request.params.type](request)
    class Meta:
        param_fields = (
            ('info', fields.DictField(label=_('查询条件'), default={})),
            ('building_list', fields.ListField(label=_('楼列表'), default=[])),
            ('type', fields.CharField(label=_('查询类型'), default="filter_building_all")),

        )


@site
class GradeManage(CoolBFFAPIView):
    name = _('班级数据管理')
   
    def fileter_grades_by_name(self,request):
        # 通过班级编号获取班级ID和name信息
        grades_list = request.params.grades_list
        grades = models.Grade.objects.filter(name__in=grades_list).values('id','name')
        return list(grades)

    def get_users_by_grade_id(self,request):
        # 根据班级ID获取班级内的学生学号
        users = models.GradeUser.objects.filter(grade__id = request.params.grade_id).values_list('username',flat=True)
        return list(users)

    def get_users_by_grade_name(self,request):
        # 根据班级名称获取班级内的学生学号
        users = models.GradeUser.objects.filter(grade__name = request.params.grade_name).values('username',flat=True)
        return list(users)
    
    def get_users_by_grade_names(self,request):
        # 根据班级名称获取班级内的学生学号
        grades = request.params.grade_name_list
        users = models.GradeUser.objects.filter(grade_id__in = grades).values('username','grade')
        return list(users)
    def get_grade_of_user(self,request):
        # 获取用户的班级
        return models.GradeUser.objects.get(username=request.params.username).grade.id
    def get_grade_user_all(self,request):
        # 获取所有用户的班级
        return list(models.GradeUser.objects.all().values('username','grade_id'))
    def get_context(self, request, *args, **kwargs):
        fun = {}
        fun['fileter_grades_by_name'] = self.fileter_grades_by_name
        fun['get_users_by_grade_name'] = self.get_users_by_grade_name
        fun['get_users_by_grade_names'] = self.get_users_by_grade_names
        fun['get_users_by_grade_id'] = self.get_users_by_grade_id
        fun['get_grade_of_user'] = self.get_grade_of_user
        fun['get_grade_user_all'] = self.get_grade_user_all
        return fun[request.params.type](request)

# run_init()
urls = site.urls
urlpatterns = site.urlpatterns + urlpatterns_dormitory
