'''
晚自修
'''


import datetime
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
        now = datetime.datetime.now()
        data = models.Record.objects.filter(task=self.task,manager=None,star_time__date=datetime.date(now.year, now.month,now.day))
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

    def submit(self,data,worker_user):
        '''点名提交
        flg: 点名状态 在/不在
        '''

        if data['type'] == 1:
            self.submit_discipline(data,worker_user)
            return
            

        flg = data['flg']
        rule_id = data['rule_id']
        # 多用户点名
        user_list = data['user_list']
        # 获取规则
        rule = models.RuleDetails.objects.get(id=rule_id)
        for u in user_list:
            user = User.objects.get(username=u)

            call,status = models.UserCall.objects.get_or_create(task=self.task,user=user,rule=rule)

            # 判断是不是本次任务第一次点名
            if call.flg == None:
                call.flg = flg
                call.save()

                # 写入考勤记录
                if not flg:
                    d = {
                        'task':self.task,
                        'rule_str':rule.name,
                        'score':rule.score,
                        'rule':rule,
                        'grade_str':user.studentinfo.grade.name,
                        'student_approved':user,
                        'worker':worker_user,
                    }

                    models.Record.objects.create(**d)
            
    def submit_discipline(self,data,worker_user):
        '''
        role_obj： 当规则为自定义的情况下 传递此参数
        rule_id_list: 规则id列表  多选规则时传递
        '''
        username = data['username']
        rule_id_list = data.get('rule_id_list',None)
        role_obj = data.get('role_obj',None)
        user = User.objects.get(username=username)

        if role_obj:
            rule_obj = models.Rule.objects.get(codename='0#003')
            rule_obj,f = models.RuleDetails.objects.get_or_create(name='违纪自定义',defaults={'rule':rule_obj,'score':1})
            d = {
              'task' : self.task,
              'rule_str' : role_obj['role_name'],
              'rule' : rule_obj,
              'score' : role_obj['role_score'],
              'grade_str' : user.studentinfo.grade.name,
              'student_approved' : user,
              'worker' : worker_user,
            }
            models.Record.objects.create(**d)
        else:
            for id in rule_id_list:
                rule = models.RuleDetails.objects.get(id=id)
                d = {
                'task' : self.task,
                'rule_str' : rule.name,
                'score' : rule.score,
                'rule' : rule,
                'grade_str' : user.studentinfo.grade.name,
                'student_approved' : user,
                'worker' : worker_user,
                }
                models.Record.objects.create(**d)

    def executor_finish(self):
        '''执行人确认任务完成'''
        pass
