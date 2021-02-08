import Apps
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls.resolvers import URLResolver, URLPattern
from collections import OrderedDict

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
    递归的去获取URL
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


    