'''
Author: 邹洋
Date: 2022-02-06 22:12:06
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-07 15:17:51
Description: 启动运行
'''
from AppInformation.models import *
from AppInformation.common.configuration import *
def run_init():
    print('分院信息初始化:')
    for c in COLLEGE_LIST:
        College.objects.get_or_create(**c)
    
    print('班级信息初始化:')
    for c in GRADE_DATA:
        o,f = Grade.objects.get_or_create(id=c['id'],college_id=c['college'])

    # for c in GRADE_USER_DATA:
    #     o,f = GradeUser.objects.get_or_create(username=c['username'],grade_id=c['grade'])
    #     #  o.grade_id = c['grade']
    #     #  o.save()
