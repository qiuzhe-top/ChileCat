
import datetime
import os
import time
from django.contrib.auth.models import User
from django.http.response import JsonResponse

from openpyxl.reader.excel import load_workbook
from .. import models

from . import knowing, health, late
'''
任务公共类
'''
task_factory = {
    '0': knowing.Knowing,
    '1': health.Health,
    '2': late.Late
}


class TaskManage(object):

    def __init__(self,task_id=None):
        if task_id:
            self.task = models.Task.objects.get(id=int(task_id))
        else:
            self.task = None
    def create_task(self,task,ids):
        '''创建任务
        '''
        task_factory[task.types](task).task_create(ids)
        
    def add_admin(self):
        '''添加管理员
        '''
        pass

    def switch(self,id):
        '''任务开启
        '''
        task = self.task
        task.is_open = not task.is_open
        flg = task.is_open
        task.save()
        return flg

    def clear_task(self):
        '''清除任务状态
        '''
        task = self.task
        return task_factory[task.types](task).clear_task()
    # def task_create(self):

    def scheduling(self,roster):
        '''保存班表
        '''
        task = self.task
        return task_factory[task.types](task).scheduling(roster)
        

    def task_roomInfo(self,type,user,floor_id,room_id):
        '''获取任务数据
        '''
        task = self.task
        if not models.TaskPlayer.objects.filter(task=task,user=user).exists():
            return ''
        if type == 0:
            return task_factory[task.types](task).storey()
        elif type == 1:
            return  task_factory[task.types](task).room(floor_id)
        elif type == 2:
            return  task_factory[task.types](task).room_students(room_id)


    def submit(self,data,worker_user):
        '''任务提交
        ''' 
        if self.task.is_open:
            return task_factory[self.task.types](self.task).submit(data,worker_user)
        return 4001

    def condition(self):
        '''查看考勤工作情况
        '''
        return task_factory[self.task.types](self.task).condition()

    def undo_record(self,record_id,worker_user):
        '''销假
        '''
        # TODO: 需要传递任务ID 并且判断是否为任务创建者或者管理员
        record = models.Record.objects.get(task=self.task,id=record_id)
        record.manager=worker_user
        record.save()
        return '销假成功'

    def early_sign(self,excel):
        """针对寝室表"""
        pass


    
    def in_zaoqian_excel(self,request):
        """导入早签数据"""
        file = request.data['file']

        # file_name = str(time.time())+ '__' +file.name
        # file_path = os.path.join('upload', file_name)
        
        # f = open(file_path,'wb')
        # for i in file.chunks():   #chunks方法是一点点获取上传的文件内容
        #     f.write(i)
        # f.close()

        # file_name = 'upload//' + file_name

        # return JsonResponse({})
        
        wb = load_workbook(file,read_only=True)

        error_list=[]
        for rows in wb:
            for row in rows:#遍历行
                username = row[0].internal_value
                name = row[1].internal_value
                str_time = row[3].internal_value
                is_header = username.find('考勤') != -1 or username.find('统计') != -1 or username.find('员工号') != -1
                if not (username == None or name == None or str_time == None) and not is_header:
                    print(username)
                    try:
                        u = User.objects.get(username=username)
                        try:
                            str_time = datetime.datetime.strptime(str_time,'%Y/%m/%d')
                            d = {
                                'rule_str':'旷早签',
                                'student_approved':u,
                                'score':1,
                                'star_time':str_time
                            }
                            sa,flg = models.Record.objects.get_or_create(**d)
                            sa.worker =  request.user
                            sa.save()
                        except:
                            error_list.append({
                                'username':username,
                                'name':name,
                                'str_time':str_time,
                                'message':'导入记录失败'
                            })
                    except:
                        error_list.append({
                            'username':username,
                            'name':name,
                            'str_time':str_time,
                            'message':'用户不存在'
                        })

        ret = {
            'message': '添加成功 请检查添加结果',
            'code':'2000',
            'data':error_list
        }
        return ret
        # return JsonResponse(ret)