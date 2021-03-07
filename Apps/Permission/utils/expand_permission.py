"""权限初始化,自动添加api"""
# import Apps
from collections import OrderedDict
from django.utils.module_loading import import_string
from django.urls.resolvers import URLResolver, URLPattern
from django.contrib.auth.models import Permission,Group
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from rest_framework.views import exception_handler
from Apps.Permission.models import ApiPermission, OperatePermission
from django.contrib.auth.models import User

# from django.shortcuts import get_object_or_404
# 自定义认证错误时的返回格式
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['code'] = 5500 if (
                response.data['detail'] == '用户认证失败'
        ) else (
            response.status_code
        )
        # response.data['code'] = response.status_code
        response.data['message'] = response.data['detail']
        del response.data['detail']  # 删除detail字段
    return response


def get_obj(app, object_name, name):
    """
    反射获取成员
    :param app: Django App 名称
    :param object_name: 视图CBV的类
    :param name: 视图类的变量
    """
    pack = __import__("Apps." + app + ".views", fromlist=True)
    class_obj = getattr(pack, object_name)
    # try:
    return getattr(class_obj, name, [])
    # except:
        # return []
        


# API 权限管理
def init_api_permissions():
    """
    根据当前URL路由自动初始化API权限
    """
    method = {'get', 'post', 'put', 'delete'}
    method_no = method.union({'', None})
    url_dic = get_all_url_dict()
    for key, value in url_dic.items():
        # TODO 添加环节
        for item in method:
            url = key + ':' + item.upper()
            name = url if len(value) == 0 or value[0] in method_no else value[0] + ':' + item.upper()
            is_auth = '*' + item in value
            is_verify = True if is_auth else item in value
            add_api_permission(url, name, is_verify,is_auth)
            # print(url,name,is_verify,is_auth)
        # name = v[0]
        # if name in method or name in ['',None]:
        #     name = k
        # if len(v)>0:
        #     method_public = method.intersection(set(v))
        #     for item in method:
        #         flag = item in method_public
        #         add_api_permission(k+':'+item.upper(),name,flag)
        # else:
        #     for item in method:
        #         add_api_permission(k+':'+item.upper(),'',False)

def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    递归获取URL
    :param per_namespace: namespace前缀，以后用户拼接name
    :param per_url: url前缀，以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    :return:
    """
    for item in urlpatterns:
        if pre_namespace == 'admin':
            continue
        url = pre_url + str(item.pattern)
        if isinstance(item, URLPattern):  # 非路由分发
            if not item.name:
                # url_ordered_dict[url] = []
                continue
            # TODO mark
            url_ordered_dict[url] = get_obj(pre_namespace, item.name, 'API_PERMISSIONS')
            # print("url字典", url_ordered_dict)
        elif isinstance(item, URLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = '%s:%s' % (pre_namespace, item.namespace)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(
                namespace, pre_url + str(item.pattern), item.url_patterns, url_ordered_dict
            )


def get_all_url_dict():
    """
    获取项目中所有
    需要验证的URL
    :return:
    """
    url_ordered_dict = OrderedDict()
    main_urls = import_string(settings.ROOT_URLCONF)
    recursion_urls(None, '/', main_urls.urlpatterns, url_ordered_dict)  # 递归去获取所有的路由
    return url_ordered_dict


def add_permission(content_type, codename, name):
    """
    添加权限
    """
    return Permission.objects.update_or_create(
        codename=codename,
        content_type=content_type,
        defaults={'name': name}
    )


def add_api_permission(codename, name, is_verify,is_auth):
    """
    添加接口权限
    """
    content_type = ContentType.objects.get_for_model(ApiPermission)
    permission, flag = add_permission(content_type, codename, name)
    ApiPermission.objects.update_or_create(permission=permission, defaults={'is_verify': is_verify,'is_auth': is_auth})


def clean_api_permission():
    """清空接口"""
    ApiPermission.objects.delete()



# 功能权限管理
def add_fun_permission(codename, name):
    """功能权限管理"""
    content_type = ContentType.objects.get_for_model(OperatePermission)
    permission, flag = add_permission(content_type, codename, name)
    OperatePermission.objects.update_or_create(permission=permission)


def init_operate_permissions():
    """功能权限管理"""
    permissions_list = {
        'OPERATE_KNOWING': '查寝点名',
        'OPERATE_HEALTH': '卫生检查',
        'OPERATE_LATE': '晚自修检查',
        'OPERATE_ASK_CLASS': '请假条管理-班主任',
        'OPERATE_ASK_TUTOR': '请假条管理-辅导员',
        'OPERATE_ASK_COURT': '请假条管理-院领导',
        'OPERATE_MONITOR_VIEW': "班委查看请假条",
    }
    for key, value in permissions_list.items():
        add_fun_permission(key, value)

# 用户组
def group_init(groups):
    '''添加用户组'''
    v = []
    for name in groups:
        obj = Group(name=name)
        v.append(obj)
    Group.objects.bulk_create(v)

def group_add_permission(group,permissions):
    '''用户组添加一组权限'''
    v = Permission.objects.filter(codename__in=permissions)
    Group.objects.get(name=group).permissions.add(*list(v))


def group_add_user(group,users):
    '''用户组添加一组用户'''
    v = User.objects.filter(username__in=users)
    Group.objects.get(name=group).user_set.add(*list(v))
