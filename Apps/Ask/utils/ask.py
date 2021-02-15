'''根据权限处理请假条'''
from django.contrib.auth.models import AnonymousUser
from Apps.Ask import ser
from Apps.Ask.models import Ask


class AskOperate():
    '''不要为了设计模式而写设计模式,虽然只是复习'''
    __statement = "接口类"
    _ask_list = Ask.objects.none()
    _user = AnonymousUser
    _ask_id = Ask.objects.none()
    def __init__(self,askid=0):
        self._ask_id = askid
    def view(self):
        '''查看'''
        try:
            self._ask_list = Ask.objects.get(id=self._ask_id)
        except Ask.DoesNotExist as ask_unexist:
            return ask_unexist
        return ser.AskSerializer(instance=self._ask_list).data

class AskToTeacher(AskOperate):
    '''
    老师->请假条
    '''
    def __init__(self, user,askid=0):
        super().__init__(askid)
        AskOperate._user = user
        AskOperate._ask_list = Ask.objects.filter(pass_id=self._user)
        # AskOperate._ask_id = askid
    def view(self):
        print("老师查看请假条")
        return ser.AskSerializer(instance=self._ask_list,many=True).data
    def undopass(self):
        '''老师不批准请假条'''
    def dopass(self):
        '''老师通过请假条'''

class AskToStudent(AskOperate):
    '''
    学生->请假条
    '''
    def __init__(self,user,askid=0):
        super().__init__(askid)
        AskOperate._user = user
        AskOperate._ask_list = Ask.objects.filter(user_id=self._user)
        # AskOperate._ask_id = askid
    def view(self):
        print("学生查看请假条")
        return ser.AskSerializer(instance=self._ask_list,many=True).data
    def submit(self):
        '''学生提交请假条'''

    def delete(self):
        '''学生删除请假条'''
        try:
            Ask.objects.get(id=self._ask_id).delete()
        except Ask.DoesNotExist as ask_unexist:
            return ask_unexist
        return True
    def modify(self):
        '''学生修改请假条'''
