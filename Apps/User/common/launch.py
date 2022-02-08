'''
Author: 邹洋
Date: 2022-02-06 22:12:06
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 10:22:33
Description: 启动运行
'''
from Apps.User.common.configuration import *
from . import utils
# 用户组初始化
def group_init():
    '''用户组初始化'''
    print('用户组初始化:')
    names = [
        # 考勤任务管理 # 后台导航栏是否展示 <考勤系统> 父选项
        'task_admin',
        # 考勤数据管理
        'task_data',
        # 检查卫生
        'health_admin',
        # 晚自修
        'late_admin',
        # 晚查寝
        'knowing_admin',
    ]
    d = utils.group_init(names)
    ret = {"message": d, "names": names}
    return ret


def init_Attendance_group():
    '''考勤权限分组'''
    print('考勤权限分组:')
    # task_data 组
    name3 = 'task_data'
    per3 = [
        'undo_record_admin',
        'zq_data_import',
    ]
    utils.group_add_permission(name3, per3)
    return 2000


def run_init():
    # print(group_init())
    # print(init_Attendance_group())

    # UseCache().init_data()
    pass


