from collections import OrderedDict
from django.http.response import JsonResponse
from django.utils.module_loading import import_string
from django.urls.resolvers import URLResolver, URLPattern
from django.contrib.contenttypes.models import ContentType
from Manage.models_extension.models_permission import ApiPermission
from django.conf import settings
from django.contrib.auth.models import Permission

'''
    获取系统所有的URL拼接成权限字符保存到数据库
'''
def init_api_permissions(request=None):
    """
    根据当前URL路由自动初始化API权限
    is_auth ： 公共接口是否需要登录
    """
    ret = {"code":2000}
    method = {'get', 'post', 'put', 'delete'}
    method_no = method.union({'', None})
    url_dic = get_all_url_dict()
    apis = []
    for key, value in url_dic.items():
        for item in method:
            url = key + ':' + item.upper()
            name = url if len(value) == 0 or value[0] in method_no else value[0] + ':' + item.upper()
            is_auth = '*' + item in value
            n = 1 if is_auth else 2 if item in value and len(value) > 0 else 3
            apis.append([url, name, n])
    add_api_permission(apis)
    return JsonResponse(ret)

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
                continue
            # TODO mark
            url_ordered_dict[url] = get_obj(pre_namespace, item.name, 'API_PERMISSIONS')
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


def add_api_permission(apis):
    """
    添加接口权限
    """
    content_type = ContentType.objects.get_for_model(ApiPermission)
    for i in apis:
        permission = add_permission(content_type, i[0], i[1])[0]
        ApiPermission.objects.update_or_create(permission=permission, defaults={'is_verify': i[2]})


def add_permission(content_type, codename, name):
    """
    根据模型
    添加权限
    """
    return Permission.objects.update_or_create(
        codename=codename,
        content_type=content_type,
        defaults={'name': name}
    )


def get_obj(app, object_name, name):
    """
    反射获取成员
    :param app: Django App 名称
    :param object_name: 视图CBV的类
    :param name: 视图类的变量
    """
    pack = __import__("Apps." + app + ".views", fromlist=True)
    class_obj = getattr(pack, object_name)
    return getattr(class_obj, name, [])



def clean_api_permission():
    """清空接口"""
    ApiPermission.objects.delete()


def check_url_exclude(url):
    """
    排除一些特定的URL
    :param url:
    :return:
    """
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True
