'''
Author: 邹洋
Date: 2021-07-06 20:59:02
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-07-06 20:59:31
Description: 
'''
from django.utils import translation


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
