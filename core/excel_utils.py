'''
Author: 邹洋
Date: 2021-07-04 13:57:48
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-26 13:40:16
Description: Excel 操作
'''

import datetime
import os
from io import BytesIO
from typing import Pattern

import xlwt
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from openpyxl import load_workbook

from core.settings import *


def list_to_excel(data,name,header,is_first_line=True):
    '''
    '''
    response = HttpResponse(content_type='application/vnd.ms-excel')
    filename = datetime.date.today().strftime("%Y-%m-%d") + name + '.xls'
    response['Content-Disposition'] = (
        'attachment; filename={}'.format(escape_uri_path(filename))
    )
    if data:
        ws = xlwt.Workbook(encoding='utf-8')
        w = ws.add_sheet('sheet1')
        index = 0
        for i in header:
            w.write(0, index, i)
            index+=1
            # w.write(0, 1, u'楼号')
            # w.write(0, 2, u'班级')
            # w.write(0, 3, u'学号')
            # w.write(0, 4, u'姓名')
            # w.write(0, 5, u'原因')
        row = 1
        for item in data:
            column = 0
            for j in item:
                w.write(row, column, j)
                column += 1
            row += 1
        # 循环完成
        output = BytesIO()
        ws.save(output)
        output.seek(0)
        response.write(output.getvalue())
    return response

def excel_to_list(request,is_first_line=True):
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
                    if i.value:
                        l.append(str(i.value))
                    else:
                        l.append(None)
                data.append(l)
    if is_first_line:
        return data
    else:
        return data[1:]



def at_all_out_xls(data):
    '''学生考勤信息记录.xls模板'''
    addr = os.getcwd()+ "/core/file/学生考勤信息记录.xlsx"
    # 设置文件 mingc
    # 打开文件
    wb = load_workbook(addr)
    # 创建一张新表
    ws = wb[wb.sheetnames[0]]
    # 第一行输入
    for i in data:
        k = dict(i)
        ws.append([
            k.get('grade',''),
            k.get('usernames',''),
            k.get('name',''),
            # 晨点
            k.get(RULE_CODE_08+'score',0),
            k.get(RULE_CODE_08+'rule',''),
            # 晨跑
            k.get(RULE_CODE_09+'score',0),
            k.get(RULE_CODE_09+'rule',''),
            # 早签
            k.get(RULE_CODE_04+'score',0),
            k.get(RULE_CODE_04+'rule',''),
            # 晚签
            k.get(RULE_CODE_02+'score',0),
            k.get(RULE_CODE_02+'rule',''),
            # 晚自修违纪
            k.get(RULE_CODE_03+'score',0),
            k.get(RULE_CODE_03+'rule',0),
            # 查寝
            k.get(RULE_CODE_01+'score',0),
            k.get(RULE_CODE_01+'rule',''),
            # 课堂
            k.get(RULE_CODE_05+'score',0),
            k.get(RULE_CODE_05+'rule',''),
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
    filename = datetime.date.today().strftime("%Y-%m-%d") + ' 学生考勤表.xls'
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

