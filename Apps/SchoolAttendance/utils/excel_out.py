
import datetime
import os
from io import BytesIO
import xlwt
from django.utils.encoding import escape_uri_path
from django.http import JsonResponse, HttpResponse
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
        w.write(0, 1, u'姓名')
        w.write(0, 2, u'总分')
        w.write(0, 3, u'学号')
        w.write(0, 4, u'详情')
        row = 1
        for i in data:
            k = dict(i)
            column = 0
            for j in k.values():
                w.write(row, column, j)
                column += 1
            row += 1
        # 循环完成
        path = os.getcwd()
        # ws.save(path + "/leaksfile/{}".format(filename))
        output = BytesIO()
        ws.save(output)
        output.seek(0)
        response.write(output.getvalue())
        print("导出excel")
        return response

