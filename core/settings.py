'''
Author: 邹洋
Date: 2021-08-20 09:06:00
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-26 18:51:06
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
PASSWOED_123456 = (
    'pbkdf2_sha256$216000$EdbBhgrAllGw$10q+5fYrzMXRnUaj/5QYKptd+6VHtBlIUc83OF9yuRE='
)

# 早签
MORNING_SIGN = '早签'

# 初始化规则
INIT_RULES = [
    {
        "rule_f": {
            'name': '查寝',
            'codename': RULE_CODE_01,
            'is_person': True,
        },
        "rules": [
            {'name': '请假', 'score': '1'},
            {'name': '无故', 'score': '1'},
        ],
    },
    {
        "rule_f": {
            'name': '晚签',
            'codename': RULE_CODE_02,
            'is_person': True,
        },
        "rules": [
            {'name': '旷一', 'score': '1'},
            {'name': '旷二', 'score': '1'},
        ],
    },
    {
        "rule_f": {
            'name': '晚自修违纪',
            'codename': RULE_CODE_03,
            'is_person': True,
        },
        "rules": [
            {'name': '睡觉', 'score': '1'},
            {'name': '玩手机', 'score': '1'},
            {'name': '讲话', 'score': '1'},
        ],
    },
    {
        "rule_f": {
            'name': MORNING_SIGN,
            'codename': RULE_CODE_04,
            'is_person': True,
        },
        "rules": [
            {'name': MORNING_SIGN, 'score': '1'},
        ],
    },
    {
        "rule_f": {
            'name': '课堂',
            'codename': RULE_CODE_05,
            'is_person': True,
        },
        "rules": [
            {'name': '早退', 'score': '1'},
        ],
    },
    {
        "rule_f": {
            'name': '宿舍卫生',
            'codename': RULE_CODE_06,
            'is_person': True,
        },
        "rules": [
            {
                'name': '寝室布局',
                'score': '10',
                'child': [
                    {'name': '布局合理美观', 'score': '7'},
                    {'name': '寝室有异味', 'score': '3'},
                ],
            },
            {
                'name': '地面',
                'score': '30',
                'child': [
                    {'name': '地面有垃圾，垃圾未及时处理', 'score': '7'},
                    {'name': '地面脏，未拖地', 'score': '8'},
                    {'name': '物品摆放不整齐', 'score': '15'},
                ],
            },
            {
                'name': '阳台卫生间',
                'score': '25',
                'child': [
                    {'name': '物品摆放不整齐', 'score': '5'},
                    {'name': '地面有垃圾', 'score': '5'},
                    {'name': '地面脏未拖', 'score': '5'},
                    {'name': '洗漱台脏，不整洁', 'score': '5'},
                    {'name': '便池有明显污垢', 'score': '5'},
                ],
            },
            {
                'name': '其他',
                'score': '5',
                'child': [
                    {'name': '未张贴寝室值日表', 'score': '2'},
                    {'name': '未张贴文明寝室建设规定', 'score': '3'},
                ],
            },
            {
                'name': '直接认定为不合格',
                'score': '400',
                'child': [
                    {'name': '其他违反学生手册行为', 'score': '100'},
                ],
            },
        ],
    },
    {
        "rule_f": {
            'name': '宿舍个人卫生',
            'codename': RULE_CODE_07,
            'is_person': True,
        },
        "rules": [
            # {
            #     'name': '床铺整洁',
            #     'score': '15',
            #     'child': [
            #     ],
            # },
            # {
            #     'name': '桌椅整洁',
            #     'score': '15',
            #     'child': [
            #     ],
            # },
            {'name': '被子未叠', 'score': '5'},
            {'name': '床上有插线板', 'score': '5'},
            {'name': '床边悬挂衣物', 'score': '5'},
            {'name': '桌面物品摆放', 'score': '10'},
            {'name': '桌面整洁', 'score': '5'},
            {'name': '拥有或使用违章电器', 'score': '100'},
            {'name': '私拉电线', 'score': '100'},
            {'name': '饲养宠物', 'score': '100'},
        ],
    },
]
