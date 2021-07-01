from django.contrib.auth.models import Permission,Group,User

def group_init(groups):
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


def group_add_permission(group, permissions):
    """用户组添加一组权限"""
    v = Permission.objects.filter(codename__in=permissions)
    Group.objects.get(name=group).permissions.add(*list(v))


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
