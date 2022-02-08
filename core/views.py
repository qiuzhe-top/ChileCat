'''
Author: 邹洋
Date: 2021-07-06 20:59:02
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 10:51:37
Description: 父类
'''
import datetime
import json
import re
from typing import Any

# from Apps.SchoolAttendance.models import *
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, utils
from cool.views.exceptions import CoolAPIException
from cool.views.view import CoolBFFAPIView
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from rest_framework import fields, utils
from Core.common.excel import *
# from django_redis import get_redis_connection

User = get_user_model()


# def create_custom_rule(codename,name,score=1):
#         '''创建自定义规则'''
#         rule_obj = Rule.objects.get(codename=codename)
#         rule_obj, f = RuleDetails.objects.get_or_create(
#             name=name, defaults={'rule': rule_obj, 'score': score}
#         )
        
#         return rule_obj

def get_end_date(request):
    end_date = request.params.end_date
    if end_date:
        end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    else:
        now = datetime.datetime.now()
        t = datetime.datetime(now.year, now.month, now.day)
        end_date = datetime.datetime(t.year, t.month, t.day, 23, 59, 59) #默认今天24点
    return end_date

def get_start_date(request):
    start_date = request.params.start_date
    if not start_date:
        now = datetime.datetime.now()
        t = datetime.datetime(now.year, now.month, now.day)
        start_date = datetime.datetime(t.year, t.month, t.day) #默认今天
    return start_date
class EditMixin:

    model = None
    edit_fields = []

    @classmethod
    def get_extend_param_fields(cls):
        ret = list()
        ret.extend(super().get_extend_param_fields())
        if cls.model is not None:
            for edit_field in cls.edit_fields:
                ret.append(
                    (
                        edit_field,
                        utils.get_rest_field_from_model_field(
                            cls.model, edit_field, default=None
                        ),
                    )
                )
        return tuple(ret)

    def get_obj(self, request):
        raise NotImplementedError

    def modify_obj(self, request, obj):
        for edit_field in self.edit_fields:
            value = getattr(request.params, edit_field, None)
            if value is not None:
                setattr(obj, edit_field, value)

    def save_obj(self, request, obj):
        obj.full_clean()
        obj.save_changed()

    def serializer_response(self, data, request):
        return self.response_info_serializer_class(data, request=request).data

    def get_context(self, request, *args, **kwargs):
        with translation.atomic():
            obj = self.get_obj(request)
            self.modify_obj(request, obj)
            self.save_obj(request, obj)
        return self.serializer_response(obj, request=request)


class PermissionView(CoolBFFAPIView):

    need_permissions = ()

    def get_context(self, request, *args, **kwargs):
        raise NotImplementedError

    def check_api_permissions(self, request, *args, **kwargs):
        if not isinstance(request.user, User):
            raise CoolAPIException(ErrorCode.ERR_DEMO_NOLOGIN)
        for permission in self.need_permissions:
            if not request.user.has_perm(permission):
                raise CoolAPIException(ErrorCode.ERR_DEMO_PERMISSION)
    class Meta:
        path = '/'


    
class ExcelInData(PermissionView,ExcelBase):
    '''
    获取和学生有关的Excel表格
    '''
    def init(self,request):
        self.db_users = {}
        self.message_list = []
        self.rows = self.excel_to_list(request)
        self.init_excel_user()
    
    def init_excel_user(self):
        # 获取涉及的学生对象列表

        user_usernams = []
        for row in self.rows:
            username = row['username']
            user_usernams.append(username)

        query = User.objects.filter(username__in=user_usernams)
        for u in query:
            self.db_users[u.username.upper()] = u

        rows_ = []
        for row in self.rows:
            username = row['username']
            name = row['name']
            # TODO 检查是否包含关键数据
            try:
                u = self.db_users[username]
            except:
                self.add_message(username,self.get_name(username),'用户不在系统')
                continue
            
            if name != None and name != u.name:
                self.add_message(username,name,'学号与姓名不一致 系统内部为:'+u.name)
                continue

            try:
                u.grade.name
            except:
                self.add_message(username,self.get_name(username),'用户没有班级信息异常')
                continue

            row['username'] = row['username'].upper()
            rows_.append(row)
        self.rows = rows_

    def add_message(self,*d):
        self.message_list.append(d)

    def get_name(self,name):
        # 获取用户实例
        try:
            return self.db_users[name].name
        except:
            return name

    def time_formatting(self,time):
        # 表格时间格式化为 2000/1/1 
        if '-' in time:
            time = time.split(' ')[0]
            time = time.replace('-','/')

        year = time.split('/')[0]
        month = int(time.split('/')[1])
        data = int(time.split('/')[2])
        time = year + '/' +str(month) +'/'+ str(data)   
        return time  

    def time_format_one(self,time):
        '''
        字符串转datetime对象

        Args:
            time (str): '2021-10-01 13:59:59.999'

        Returns:
            [type]: [description]
        '''
        time = time.split('.')[0]
        f = '%Y-%m-%d %H:%M:%S'
        t = datetime.datetime.strptime(time,f)
        if t.minute==59 and t.second == 59:
            t += datetime.timedelta(seconds=1)
        return t
    class Meta:
        path = '/'

class InitCacheConnection:
    '''
    获取redis连接
    https://www.cnblogs.com/jiyu-hlzy/p/11980427.html
    '''
    def __init__(self) -> None:
        self.init_cache()
        
    def init_cache(self, cache=None):
        '''
        获取redis连接
        '''
        if not cache:
            if not hasattr(self,'cache'):
                self.cache = 1#get_redis_connection()
        else:
            self.cache = cache
        return self
