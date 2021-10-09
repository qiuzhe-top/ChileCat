'''
Author: 邹洋
Date: 2021-09-08 19:34:17
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-10-09 10:33:06
Description: 
'''
import datetime


def is_number(s):
    '''判断字符串是否为数字'''
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def get_end_date(request):
    end_date = request.params.end_date
    if end_date:
        end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    else:
        now = datetime.datetime.now()
        t = datetime.datetime(now.year, now.month, now.day)
        end_date = datetime.datetime(t.year, t.month, t.day, 23, 59, 59) #默认今天24点
    return end_date

def get_start_date(request):
    start_date = request.params.start_date
    if not start_date:
        now = datetime.datetime.now()
        t = datetime.datetime(now.year, now.month, now.day)
        start_date = datetime.datetime(t.year, t.month, t.day) #默认今天
    return start_date