'''
Author: 邹洋
Date: 2021-07-04 13:57:48
Email: 2810201146@qq.com
LastEditors: OBKoro1
LastEditTime: 2021-07-04 14:36:13
Description: Excel 操作
'''

import datetime
import os
from io import BytesIO
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



# 考勤汇总数据导出
def at_all_out_xls(data):
        response = HttpResponse(content_type='application/vnd.ms-excel')
        filename = datetime.date.today().strftime("%Y-%m-%d") + ' 学生缺勤表.xls'
        response['Content-Disposition'] = (
            'attachment; filename={}'.format(escape_uri_path(filename))
        )
        ws = xlwt.Workbook(encoding='utf-8')
        w = ws.add_sheet('sheet1')
        w.write(0, 0, u'班级')
        w.write(0, 1, u'学号')
        w.write(0, 2, u'姓名')

        w.write(0, 3, u'查寝')
        w.write(0, 4, u'晚签')
        w.write(0, 5, u'晚自修违纪')
        w.write(0, 6, u'早签')
        w.write(0, 7, u'课堂')
        w.write(0, 8, u'总分')

        w.write(0, 9, u'查寝')
        w.write(0, 10, u'晚签')
        w.write(0, 11, u'晚自修违纪')
        w.write(0, 12, u'早签')
        w.write(0, 13, u'课堂')
        row = 1
        for i in data:
            k = dict(i)
            column = 0
            try:
                w.write(row, 0, k.get('grade',None))
                w.write(row, 1, k.get('usernames',None))
                w.write(row, 2, k.get('name',None))
                w.write(row, 3, k.get('0#001score',None))
                w.write(row, 4, k.get('0#002score',None))
                w.write(row, 5, k.get('0#003score',None))
                w.write(row, 6, k.get('0#004score',None))
                w.write(row, 7, k.get('0#005score',None))
                w.write(row, 8, k.get('score',None))
                w.write(row, 9, k.get('0#001rule',None))
                w.write(row, 10,k.get('0#002rule',None))
                w.write(row, 11, k.get('0#003rule',None))
                w.write(row, 12, k.get('0#004rule',None))
                w.write(row, 13, k.get('0#005rule',None))
            except:
                w.write(row, 0, k.get('usernames',None))
                w.write(row, 1, k['导出异常'])
            row += 1
        # 循环完成
        path = os.getcwd()
        # ws.save(path + "/leaksfile/{}".format(filename))
        output = BytesIO()
        ws.save(output)
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
