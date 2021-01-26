'''管理视图'''
import xlrd
from rest_framework.views import APIView

# Create your views here.

class ImportExcel(APIView):
    '''从excel导入数据'''
    def post(self,request):
        '''导入学生数据'''
        file = request.FILES.get('file')
        wb = xlrd.open_workbook(filename=None,file_contents=file.read())
        table = wb.sheets()[0]
        nrows = table.nrows
