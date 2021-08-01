'''
Author: 邹洋
Date: 2021-07-06 20:59:02
Email: 2810201146@qq.com
LastEditors: Please set LastEditors
LastEditTime: 2021-08-01 21:40:19
Description: 父类
'''
import json

from django.db.models.query_utils import Q

from Apps.SchoolAttendance.models import *
from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, utils
from cool.views.exceptions import CoolAPIException
from cool.views.view import CoolBFFAPIView
from django.contrib.auth.models import User
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from rest_framework import fields, utils


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


class Permission(CoolBFFAPIView):

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


class TaskBase(Permission):

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
            return self.task
        except:
            raise CoolAPIException(ErrorCode.ERR_TAKS_IS_NO)

    def get_task_by_user(self):
        '''通过用户和任务id获取任务'''
        try:
            id = self.request.params.task_id
            user = self.request.user
            self.task = Task.objects.get(id=int(id),admin=user)
            return self.task
        except:
            raise CoolAPIException(ErrorCode.ERR_TAKS_USER_HAS_NO_TASK)
    
    def get_task_player_by_user(self):
        '''通过用户和任务id获取任务'''
        try:
            id = self.request.params.task_id
            user = self.request.user
            self.task = TaskPlayer.objects.get(task=int(id),user=user).task
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
