'''
Author: 邹洋
Date: 2021-08-20 09:06:00
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-10-01 13:02:32
Description: 系统配置
'''
# 用户初始密码 123456加密后的密码
PASSWOED_123456 = (
    'pbkdf2_sha256$216000$EdbBhgrAllGw$10q+5fYrzMXRnUaj/5QYKptd+6VHtBlIUc83OF9yuRE='
)
# 早签
MORNING_SIGN = '早签'
MORNING_POINT = '晨点'
MORNING_RUNNING = '晨跑'

# 分院数据初始化
ZHJT_NAME = '智慧交通学院'
ZHJT_CODENAM = 'ZHJT'
LQ_NAME = '路桥学院'
LQ_CODENAM = 'LQ'

COLLEGE_LIST = [
    {'id':100, "name": ZHJT_NAME, 'codename': ZHJT_CODENAM},
    {'id':200, "name": LQ_NAME, 'codename': LQ_CODENAM},
]


# 用作自定义规则的分类 只会在第一次提交自定义规则的时候创建
CUSTOM_RULE = 'CUSTOM_RULE'
RULE_NAME_01_01 = '查寝' + CUSTOM_RULE
RULE_NAME_07_01 = '个人卫生' + CUSTOM_RULE
RULE_NAME_03_01 = '晚自修违纪' + CUSTOM_RULE
RULE_CODE_01 = '00001'
RULE_CODE_02 = '00002'
RULE_CODE_03 = '00003'
RULE_CODE_04 = '00004'
RULE_CODE_05 = '00005'
RULE_CODE_06 = '00006'
RULE_CODE_07 = '00007'
RULE_CODE_08 = '00008'
RULE_CODE_09 = '00009'
# 初始化规则
INIT_RULES = [
    {
        "rule_f": {
            'id': 100,
            'name': '查寝',
            'codename': RULE_CODE_01,
            'is_person': True,
        },
        "rules": [
            {'id': 101, 'name': '请假', 'score': 6.0},
            {'id': 102, 'name': '无故', 'score': 6.0},
            {'id': 103, 'name': RULE_NAME_01_01, 'score': 6.0},
        ],
    },
    {
        "rule_f": {
            'id': 200,
            'name': '晚签',
            'codename': RULE_CODE_02,
            'is_person': True,
        },
        "rules": [
            {'id': 201, 'name': '旷一', 'score': 1.0},
            {'id': 202, 'name': '旷二', 'score': 1.0},
        ],
    },
    {
        "rule_f": {
            'id': 300,
            'name': '晚自修违纪',
            'codename': RULE_CODE_03,
            'is_person': True,
        },
        "rules": [
            {'id': 301, 'name': '睡觉', 'score': 1.0},
            {'id': 302, 'name': '玩手机', 'score': 1.0},
            {'id': 303, 'name': '讲话', 'score': 1.0},
            {'id': 304, 'name': RULE_NAME_03_01, 'score': 1.0},
        ],
    },
    {
        "rule_f": {
            'id': 400,
            'name': MORNING_SIGN,
            'codename': RULE_CODE_04,
            'is_person': True,
        },
        "rules": [
            {'id': 401, 'name': MORNING_SIGN, 'score': 0.5},
        ],
    },

    {
        "rule_f": {
            'id': 500,
            'name': '课堂',
            'codename': RULE_CODE_05,
            'is_person': True,
        },
        "rules": [
            {'id': 501, 'name': '早退', 'score': 1.0},
        ],
    },
    {
        "rule_f": {
            'id': 600,
            'name': '宿舍卫生',
            'codename': RULE_CODE_06,
            'is_person': True,
        },
        "rules": [
            {
                'id': 601,
                'name': '寝室布局',
                'score': 10.0,
                'child': [
                    {'id': 651,'name': '布局合理美观', 'score': 7.0},
                    {'id': 652,'name': '寝室有异味', 'score': 3.0},
                ],
            },
            {
                'id': 602,
                'name': '地面',
                'score': 30.0,
                'child': [
                    {'id': 653,'name': '地面有垃圾，垃圾未及时处理', 'score': 7.0},
                    {'id': 654,'name': '地面脏，未拖地', 'score': 8.0},
                    {'id': 655,'name': '物品摆放不整齐', 'score': 15.0},
                ],
            },
            {
                'id': 603,
                'name': '阳台卫生间',
                'score': 25.0,
                'child': [
                    {'id': 656,'name': '物品摆放不整齐', 'score': 5.0},
                    {'id': 657,'name': '地面有垃圾', 'score': 5.0},
                    {'id': 658,'name': '地面脏未拖', 'score': 5.0},
                    {'id': 659,'name': '洗漱台脏，不整洁', 'score': 5.0},
                    {'id': 660,'name': '便池有明显污垢', 'score': 5.0},
                ],
            },
            {
                'id': 604,
                'name': '其他',
                'score': 5.0,
                'child': [
                    {'id': 661,'name': '未张贴寝室值日表', 'score': 2.0},
                    {'id': 662,'name': '未张贴文明寝室建设规定', 'score': 3.0},
                ],
            },
            {
                'id': 605,
                'name': '直接认定为不合格',
                'score': 400.0,
                'child': [
                    {'id': 663,'name': '其他违反学生手册行为', 'score': 100.0},
                ],
            },
        ],
    },
    {
        "rule_f": {
            'id': 700,
            'name': '宿舍个人卫生',
            'codename': RULE_CODE_07,
            'is_person': True,
        },
        "rules": [
            {'id': 701, 'name': '被子未叠', 'score': 5.0},
            {'id': 702, 'name': '床上有插线板', 'score': 5.0},
            {'id': 703, 'name': '床边悬挂衣物', 'score': 5.0},
            {'id': 704, 'name': '桌面物品摆放', 'score': 10.0},
            {'id': 705, 'name': '桌面整洁', 'score': 5.0},
            {'id': 706, 'name': '拥有或使用违章电器', 'score': 100.0},
            {'id': 707, 'name': '私拉电线', 'score': 100.0},
            {'id': 708, 'name': '饲养宠物', 'score': 100.0},
            {'id': 709, 'name': RULE_NAME_07_01, 'score': 1.0},
        ],
    },
    {
        "rule_f": {
            'id': 800,
            'name': MORNING_POINT,
            'codename': RULE_CODE_08,
            'is_person': True,
        },
        "rules": [
            {'id': 801, 'name': MORNING_POINT,'score': 1.0},
        ],
    },
        {
        "rule_f": {
            'id': 900,
            'name': MORNING_RUNNING,
            'codename': RULE_CODE_09,
            'is_person': True,
        },
        "rules": [
            {'id': 901, 'name': MORNING_RUNNING,'score': 3.0},
        ],
    },
]
