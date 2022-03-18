'''
Author: 邹洋
Date: 2022-02-06 22:12:06
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2022-02-13 11:55:04
Description: 启动运行
'''

from AppAttendance.common.configuration import *
from AppAttendance.models import Rule, RuleDetails
from django.contrib.contenttypes.models import ContentType
from core.common  import group
def init_permissions():
    print('考勤权限分组初始化完成')
    content_type = ContentType.objects.get(app_label='AppAttendance', model='task')
    for group_name in PERMISSIONS:
        group.get_or_group(group_name)
        permis = PERMISSIONS[group_name]
        for per in permis:
            per_name = permis[per]
            group.get_or_permission(per,per_name,content_type)
        if permis:
            group.group_add_permission(group_name,permis.keys())
    group.group_add_permission("task_data", ['change_record','view_record'])
def uinitialization_rules():
    '''考勤规则初始化
    codename:系统内部使用不能随意修改 导出Excel会使用
    '''
    print('晚自修规则初始化完成')
    # TODO 效率低
    res = []
    for item in INIT_RULES:
        rule_f = item['rule_f']
        rules = item['rules']
        
        rule, flg = Rule.objects.get_or_create(**rule_f) # 一级规则
        if flg:
            res.append('创建：' + rule_f['name'])
        else:
            res.append('存在：' + rule_f['name'])

        for r in rules:
            rule_detail = RuleDetails.objects.get_or_create(
                id=r['id'], name=r['name'], score=r['score'], rule=rule
            )[0] # 二级规则
            if 'child' in r.keys():
                for child_rule in r['child']:
                    child_rule['rule'] = rule
                    child_rule['parent_id'] = rule_detail
                    RuleDetails.objects.get_or_create(**child_rule) # 三级规则
    return res

def run_init():
    uinitialization_rules()
    init_permissions()