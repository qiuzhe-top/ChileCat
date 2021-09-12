'''
Author: 邹洋
Date: 2021-08-20 09:06:00
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-11 17:17:41
Description: 配置
'''

RULE_CODE_01 = '0#001'
RULE_CODE_02 = '0#002'
RULE_CODE_03 = '0#003'
RULE_CODE_04 = '0#004'
RULE_CODE_05 = '0#005'
RULE_CODE_06 = '0#006'
RULE_CODE_07 = '0#007'

# 用作自定义规则的分类 只会在第一次提交自定义规则的时候创建
CUSTOM_RULE = 'CUSTOM_RULE'
RULE_NAME_01_01 = '查寝' + CUSTOM_RULE
RULE_NAME_07_01 = '个人卫生' + CUSTOM_RULE
RULE_NAME_03_01 = '晚自修违纪' + CUSTOM_RULE

# 分院代码
ZHJT_NAME = '智慧交通学院'
ZHJT_CODENAM = 'ZHJT'
LQ_NAME = '路桥学院'
LQ_CODENAM = 'LQ'

# 用户初始密码 123456加密后的密码 
PASSWOED_123456 = 'pbkdf2_sha256$216000$EdbBhgrAllGw$10q+5fYrzMXRnUaj/5QYKptd+6VHtBlIUc83OF9yuRE='

# 早签
MORNING_SIGN = '早签'

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
            {'name': '无故', 'score': '1'},
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
            'name': MORNING_SIGN,
            'codename': RULE_CODE_04,
            'is_person': True,
        },
        "rules": [
            {'name': MORNING_SIGN, 'score': '1'},
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


