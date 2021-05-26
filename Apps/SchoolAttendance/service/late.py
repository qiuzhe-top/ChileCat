'''
晚自修
'''


import json
from django.contrib.auth.models import User
from django.db.models import indexes
from Apps.SchoolAttendance import models, serializers


class Late(object):

    
    def __init__(self, task_obj):
        if task_obj:
            self.task = task_obj
            
    def task_create(self):
        '''创建任务
        '''

        pass
    
    def clear_task(self):
        '''清除任务状态
        学生点名情况 全部置为在班
        '''
        models.UserCall.objects.filter(task=self.task).update(flg=None)
        return '执行成功'

    def scheduling(self,roster):
        '''排班
        roster:[
            {username:'19510144',name:'张三'},
            {username:'19510144',name:'张三'}
        ]
        '''
        user_list = []
        roster_new = []
        # 从班表里面获取用户
        for item in roster:
            u = User.objects.filter(username=item['username'])
            if len(u) == 1:
                user_list.append(u[0])
                roster_new.append(item)

        # 历史班表清空
        models.TaskPlayer.objects.filter(task=self.task,is_admin=False).delete()

        # 新用户进行任务绑定
        for u in user_list:
            models.TaskPlayer.objects.get_or_create(task=self.task,user=u,is_admin=False)

        self.task.roster = json.dumps(roster_new)
        self.task.save()
        return '执行成功' + '更新' + str(len(roster_new)) + '个学生' 

    def condition(self):
        '''查看考勤工作情况      
        '''
        data = models.Record.objects.filter(task=self.task)
        ser = serializers.ConditionRecord(instance=data,many=True).data
        
        return ser

    def progress(self):
        '''查看考勤进度
        '''
        pass

    def undo_record(self):
        '''销假
        '''

        pass

    def out_data(self):
        '''数据导出
        '''
        pass

    def get_task(self):
        '''执行人获取任务
        '''
        pass

    def rule(self):
        '''获取规则
        '''
        pass

    def student_information(self):
        '''获取学生信息
        '''
        pass

    def submit(self):
        '''考勤提交
        '''
        pass

    def executor_finish(self):
        '''执行人确认任务完成'''
        pass
