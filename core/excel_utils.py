'''
Author: 邹洋
Date: 2021-07-04 13:57:48
Email: 2810201146@qq.com
LastEditors: Please set LastEditors
LastEditTime: 2021-08-01 19:41:12
Description: Excel 操作
'''

import datetime
import os
from io import BytesIO
from typing import Pattern
import xlwt
from django.utils.encoding import escape_uri_path
from django.http import HttpResponse
from openpyxl import load_workbook

def excel_to_list(request):
    '''
        excel 转换为列表
        当一行的第一列为空时忽略这一行数据
    '''
    file = request.data['file']
    data = []
    wb = load_workbook(file,read_only=True)
    for rows in wb:
        for row in rows:#遍历行
            if row[0].value:
                l = []
                for i in row:
                    l.append(str(i.value))
                data.append(l)
    return data
import datetime
from random import choice
from time import time
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
def at_all_out_xls(data):
    '''学生考勤信息记录.xlsx模板'''
    addr = os.getcwd()+ "\\core\\file\\学生考勤信息记录.xlsx"
    # 设置文件 mingc
    # 打开文件
    wb = load_workbook(addr)
    # 创建一张新表
    ws = wb[wb.sheetnames[0]]
    # 第一行输入
    # ws.append(['TIME', 'TITLE', 'A-Z','TIME', 'TITLE', 'A-Z'])
    for i in data:
        k = dict(i)
        ws.append([
            k.get('grade',''),
            k.get('usernames',''),
            k.get('name',''),

            k.get('0#001score',0),
            k.get('0#001rule',''),

            k.get('0#002score',0),
            k.get('0#002rule',''),

            k.get('0#003score',0),
            k.get('0#003rule',0),

            k.get('0#004score',0),
            k.get('0#004rule',''),

            k.get('0#005score',0),
            k.get('0#005rule',''),
            0,
            '',
            k.get('score','')
        ])
    TIME = datetime.datetime.now()#.strftime("%H:%M:%S")
    ws.append(['统计时间:',TIME])
    # wb.save(addr)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = (
        'attachment; filename={}'.format(escape_uri_path("学生缺勤表.xls"))
    )
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response

# 晚查寝当日数据导出
def out_knowing_data(ser_records):
    '''晚查寝当日数据导出
    '''
    response = HttpResponse(content_type='application/vnd.ms-excel')
    filename = datetime.date.today().strftime("%Y-%m-%d") + ' 学生缺勤表.xls'
    response['Content-Disposition'] = (
        'attachment; filename={}'.format(escape_uri_path(filename))
    )
    if ser_records:
        ws = xlwt.Workbook(encoding='utf-8')
        w = ws.add_sheet('sheet1')
        w.write(0, 0, u'日期')
        w.write(0, 1, u'楼号')
        w.write(0, 2, u'班级')
        w.write(0, 3, u'学号')
        w.write(0, 4, u'姓名')
        w.write(0, 5, u'原因')
        row = 1
        for i in ser_records:
            k = dict(i)
            column = 0
            for j in k.values():
                w.write(row, column, j)
                column += 1
            row += 1
        # 循环完成
        output = BytesIO()
        ws.save(output)
        output.seek(0)
        response.write(output.getvalue())
    return response
