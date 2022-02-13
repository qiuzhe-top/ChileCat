'''
Author: 邹洋
Date: 2021-09-08 19:34:17
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-13 11:09:25
Description: 
'''
from django.contrib.auth.models import Permission,Group
from django.contrib.auth import get_user_model
User = get_user_model()

def group_bulk_create(groups):
    """添加用户组"""
    v = []
    for name in groups:
        obj = Group(name=name)
        v.append(obj)
    try:
        f = Group.objects.bulk_create(v)
        return len(f)
    except:
        return '组创建失败/可能存在已创建的内容'
        
def get_or_group(group_name):
    return Group.objects.get_or_create(name=group_name)

def get_or_permission(codename,name,content_type):
    return Permission.objects.get_or_create(codename=codename,name=name,content_type=content_type)


def group_add_permission(group_name, permissions):
    """用户组添加一组权限"""
    v = Permission.objects.filter(codename__in=permissions)
    Group.objects.get(name=group_name).permissions.add(*list(v))


def group_add_user(group, users):
    '''用户组添加一组用户'''
    v = User.objects.filter(username__in=users)
    Group.objects.get(name=group).user_set.add(*list(v))
    v.update(is_staff=True)

def group_remove_user(group, users):
    '''用户组删除一组用户'''

    user_list = User.objects.filter(username__in=users)
    
    error = []
    group = Group.objects.get(name=group)
    for u in user_list:
        u.groups.remove(group)
    return error
    
def group_clean(group_name):
    # 用户组中所有用户退出组
    group = Group.objects.get(name=group_name)
    group.user_set.clear()


def user_admin_clean(user_list):
    '''清空用户admin标识'''
    
    for item in user_list:
        User.objects.filter(username=item).update(is_staff=False)
