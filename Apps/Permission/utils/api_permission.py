import Apps
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls.resolvers import URLResolver, URLPattern
from collections import OrderedDict
from Apps.Permission.models import ApiPermission
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

def get_obj(app,object_name,name):
  '''
  反射
  :param app: Django App 名称
  :param object_name: 视图CBV的类
  :param name: 视图类的变量
  '''
  pack = __import__("Apps."+app+".views",fromlist = True)
  class_obj = getattr(pack,object_name)
  return getattr(class_obj,name,[])

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
            # if pre_namespace:
            #     name = '%s:%s' % (pre_namespace, item.name)
            # else:
            #     name = item.name
            if not item.name:
                url_ordered_dict[url] = []
                continue
            url_ordered_dict[url] = get_obj(pre_namespace,item.name,'API_PERMISSIONS')
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
            recursion_urls(namespace, pre_url + str(item.pattern), item.url_patterns, url_ordered_dict)


def get_all_url_dict():
    """
    获取项目中所有
    需要验证的URL
    :return:
    """
    url_ordered_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)
    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)  # 递归去获取所有的路由
    return url_ordered_dict

def add_permission(content_type,codename,name):
    '''
    添加权限
    '''
    obj,flag = Permission.objects.get_or_create(
        codename= codename,
        defaults={'name':name},
        content_type=content_type,
    )
    if obj.name != name:
        obj.name = name
        obj.save()
    # permission = permission(name = name)
    # permission.save()
    return obj,flag
def add_api_permission(codename,name,is_verify):
    '''
    添加接口权限
    '''
    content_type = ContentType.objects.get_for_model(ApiPermission)
    permission,flag = add_permission(content_type,codename,name)
    ApiPermission.objects.get_or_create(permission = permission,is_verify=is_verify)

def clean_api_permisson():
    Permission.objects.filter(codename__contains ='api')

def init_api_permissions():
    '''
    根据当前URL路由自动初始化API权限
    '''
    method = set(['get', 'post', 'put', 'delete'])
    url_dic = get_all_url_dict()
    for k,v in url_dic.items():
        if len(v)>0:
            name = v[0]
            if name in method:
                name = ''
            method_public = method.intersection(set(v))
            for item in method:
                flag = item in method_public
                add_api_permission(k+':'+item.upper(),name,flag)
        else:
            for item in method:
                add_api_permission(k+':'+item.upper(),'',False)