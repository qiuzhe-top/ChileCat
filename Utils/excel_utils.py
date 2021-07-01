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
