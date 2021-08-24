'''
Author: 邹洋
Date: 2021-08-20 09:06:00
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-08-20 09:23:56
Description: 配置
'''

RULE_CODE_01 = '0#001'
RULE_CODE_02 = '0#002'
RULE_CODE_03 = '0#003'
RULE_CODE_04 = '0#004'
RULE_CODE_05 = '0#005'
RULE_CODE_06 = '0#006'
RULE_CODE_07 = '0#007'

RULE_NAME_01_01 = '查寝:其他情况'
RULE_NAME_07_01 = '个人卫生:其他情况'
RULE_NAME_03_01 = '晚自修违纪:其他情况'

# 初始化规则
INIT_RULES =  [
        {
          "rule_f" :{
            'name': '查寝',
            'codename': RULE_CODE_01,
            'is_person': True,
          },
          "rules":[
            {'name': '请假', 'score': '1'},
            {'name': '未到校', 'score': '1'},
            {'name': '当兵', 'score': '1'},
          ]
      },
      {
        "rule_f":{
          'name': '晚签',
          'codename': RULE_CODE_02,
          'is_person': True,
        },
        "rules":[
          {'name': '旷一', 'score': '1'},
          {'name': '旷二', 'score': '1'},
        ]
      },
      {
        "rule_f": {
          'name': '晚自修违纪',
          'codename': RULE_CODE_03,
          'is_person': True,
        },
        "rules":[
            {'name': '睡觉', 'score': '1'},
            {'name': '玩手机', 'score': '1'},
        ]
      },
      {
        "rule_f":{
            'name': '早签',
            'codename': RULE_CODE_04,
            'is_person': True,
        },
        "rules": [
            {'name': '早签', 'score': '1'},
        ]
      },
      {
        "rule_f" : {
          'name': '课堂',
          'codename': RULE_CODE_05,
          'is_person': True,
        },
        "rules": [
            {'name': '早退', 'score': '1'},
        ]
      },
      {
        "rule_f": {
            'name': '宿舍卫生',
            'codename': RULE_CODE_06,
            'is_person': True,
        },
        "rules": [
            {'name': '地面脏乱', 'score': '1'},
            {'name': '阳台脏乱', 'score': '1'},
        ]
      },
      {
        "rule_f": {
            'name': '宿舍个人卫生',
            'codename': RULE_CODE_07,
            'is_person': True,
        },
        "rules": [
            {'name': '被子未叠', 'score': '1'},
            {'name': '鞋子摆放不合格', 'score': '1'},
        ]
      }
    ]


