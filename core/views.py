'''
Author: 邹洋
Date: 2021-07-06 20:59:02
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-12-01 14:45:16
Description: 父类
'''
from typing import Any
from core.common import is_number
import json

from django.db.models.query_utils import Q

from Apps.SchoolAttendance.models import *
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, utils
from cool.views.exceptions import CoolAPIException
from cool.views.view import CoolBFFAPIView
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from rest_framework import fields, utils
from core.excel_utils import excel_to_list
from core.models_utils import create_custom_rule

from django.contrib.auth import get_user_model
User = get_user_model()
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


class TaskBase(PermissionView):
    def get_context(self, request, *args, **kwargs):
        raise NotImplementedError
    

        
    def is_open(self):
        if not self.task.is_open:
            raise CoolAPIException(ErrorCode.ERR_TASK_ISOPEN_FALSE)
 
    def get_task(self):
        '''通过任务id获取任务'''
        try:
            id = self.request.params.task_id
            self.task = Task.objects.get(id=int(id))
            self.request.task = self.task
            return self.task
        except:
            raise CoolAPIException(ErrorCode.ERR_TAKS_IS_NO)

    def get_task_by_user(self):
        '''通过管理用户和任务id获取任务'''
        try:
            id = self.request.params.task_id
            user = self.request.user
            self.task = Task.objects.get(id=int(id),admin=user)
            self.request.task = self.task
            return self.task
        except:
            raise CoolAPIException(ErrorCode.ERR_TAKS_USER_HAS_NO_TASK)
    
    def get_task_player_by_user(self):
        '''通过工作用户和任务id获取任务'''
        try:
            id = self.request.params.task_id
            user = self.request.user
            self.task = TaskPlayer.objects.get(task=int(id),user=user).task
            self.request.task = self.task
            return self.task
        except:
            raise CoolAPIException(ErrorCode.ERR_TAKS_USER_HAS_NO_TASK)
    
    def init_scheduling(self,users,roster):
        '''初始化班表'''
        self.get_task_by_user()

        # 历史班表清空
        TaskPlayer.objects.filter(task=self.task).delete()

        # 新用户进行任务绑定
        for u in users:
            TaskPlayer.objects.get_or_create(task=self.task,user=u)

        self.task.roster=json.dumps(roster)
        self.task.save()


    class Meta:
        param_fields = (
            ('task_id', fields.CharField(label=_('任务id'), max_length=8)),
        )
        path = '/'

class RecordBase():

    def init_custom_rule(self):
        '''
        构建规则（自定义）

        Returns
        -------
        models.Rule
            规则实例
        '''        
        if self.custom_rule:
            return self.custom_rule
        else:
            self.custom_rule =self.get_custom_rule()
            return self.custom_rule

    def get_custom_rule(self):
        '''获取规则（自定义）'''
        return None

    def get_record_by_id(self,id):
        '''
        通过ID获取考勤记录

        Parameters
        ----------
        id : int
            考勤记录在数据库中的id

        Returns
        -------
        models.Record
            考勤记录对象
        '''
        return Record.objects.get(id=id)
        
    def get_record_by_id_task(self,id,task):
        '''
        通过ID获取考勤记录

        Parameters
        ----------
        id : int
            考勤记录在数据库中的id
        task : models.Task
            考勤任务实例

        Returns
        -------
        models.Record
            考勤记录对象
        '''
        return Record.objects.get(task=task, id=id)

    def undo_record(self,record,manager_user):
        '''
        单个 核销考勤记录
        通过给manager属性来表示已经核销
        这个属性记录了是谁核销
        核销判断逻辑就是根据是否存在这个属性

        Parameters
        ----------
        record : models.Record
            任务记录实例
        manager_user : models.User
            用户模型实例,Record表中manager字段
        '''             
        record.manager = manager_user
        record.save()

    def submit_record(self,record_model):
        '''
        单个 提交考勤记录
        
        '''
        Record.objects.create(**record_model)

class SubmitBase(TaskBase,RecordBase):


    def get_room(self):
        '''获取房间'''
        try:
            room_id = self.request.params.room_id
            room = Room.objects.get(id=room_id)
            self.room_str = str(room)
            # 保存房间状态为已检查
            obj, flg = RoomHistory.objects.get_or_create(room=room, task=self.task)
            if self.task.types == '0':
                obj.is_knowing = True
            elif self.task.types == '1':
                obj.is_health = True
            obj.save()
            return room
        except:
            self.room_str = None
            return None
    def submit_check(self):
        '''
        提交前数据检查
        在这里可以对考勤记录数据做最后的修改
        执行完后就进入任务提交，但如果返回False时将不会提交
        '''        
        pass
        
    def submit_undo_record(self,record_model,manager_user):
        '''
        单个 核销考勤记录
        
        Parameters
        ----------
        record_model : models.Record
            任务记录实例
        manager_user : models.User
            用户模型实例
        '''       
        self.undo_record(record_model,manager_user)
        
    def get_context(self, request, *args, **kwargs):
        # TODO 优化提交数度
        self.get_task_player_by_user()
        self.is_open()
        self.custom_rule = None
        self.get_room()
        records = request.params.records

        for record in records:
            # 获取用户
            user = None
            try:
                user = User.objects.get(id=record['user_id'])
            except:
                pass

            record_model = {}
            # 构建 考勤记录模型
            record_model['task'] = self.task
            record_model['room_str'] = self.room_str
            try:
                record_model['grade_str'] =  user.grade.name
            except:
                record_model['grade_str'] =  None
            record_model['student_approved'] = user
            record_model['worker'] = self.request.user

            status = str(record['status'])
            # 撤销记录
            if status == '1':
                record_model['manager'] = self.request.user
                self.submit_undo_record(record_model,user)                          

            # 提交记录
            elif status == '0':
                reason = record['reason'] # 自定义规则文本 / 规则ID
                reason_is_custom = record['reason_is_custom']
                
                rule_str = '' # 规则文本
                rule = None # 规则对象

                if reason_is_custom:# 判断是否为自定义规则
                    rule = self.init_custom_rule()
                    rule_str = reason
                else:
                    try:
                        rule = RuleDetails.objects.get(id=reason)
                        rule_str = rule.name
                    except:
                        rule = self.init_custom_rule()
                        rule_str = reason

                record_model['rule_str'] = rule_str
                record_model['score'] = 1 # 默认扣一分
                if rule:
                    record_model['rule'] = rule
                    record_model['score'] = rule.score

                if self.submit_check(record_model,record) != False:
                    self.submit_record(record_model)
                    

    class Meta:
        records= {}
        records['user_id'] = '用户ID'
        records['reason'] = '规则内容'
        records['status'] = '提交类型'
        records['score'] = '自定义扣分'
        records['reason_is_custom'] = '是否是自定义规则'
        
        param_fields = (
            ('records', fields.ListField(label=_('提交记录 '),default=records)),
        )
        path = '/'
        

    
class ExcelInData(PermissionView):

    def init(self,request):
        self.db_users = {}
        self.error_list = []
        self.rows = excel_to_list(request)
        self.init_excel_user()
    
    def init_excel_user(self):
        # 获取涉及的学生对象列表
        user_usernams = []
        for row in self.rows:
            username = row[0]
            user_usernams.append(username)
        query = User.objects.filter(username__in=user_usernams)
        for u in query:
            self.db_users[u.username.upper()] = u
            
    def add_error(self,username,name,time,message):
        self.error_list.append(
            {
                'username': username,
                'name': name,
                'str_time': time,
                'message': message,
            }
        )

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

    class Meta:
        path = '/'
