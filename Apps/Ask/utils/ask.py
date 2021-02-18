"""根据权限处理请假条"""
from django.contrib.auth.models import AnonymousUser
from Apps.Ask import ser
from Apps.Ask.models import Ask


class AskOperate:
    """操作主类"""
    _user = AnonymousUser
    _ask_list = Ask.objects.none()  # <QuerySet[]>

    def __init__(self, user=AnonymousUser):
        self._user = user

    def view(self, ask_id):
        """目的:查看单条"""
        try:
            self._ask_list = Ask.objects.get(id=ask_id)
            return ser.AskSerializer(instance=self._ask_list).data
        except Ask.DoesNotExist as ask_un_exist:
            print(ask_un_exist)
            return ask_un_exist

    def delete(self, ask_id):
        """删除请假条"""
        try:
            self._ask_list = Ask.objects.get(id=ask_id)
            self._ask_list.delete()
        except Ask.DoesNotExist as ask_not_exist:
            return ask_not_exist
        return True


class AskToTeacher(AskOperate):
    """
    老师->请假条
    """

    def views(self):
        print("老师查看请假条")
        AskOperate._ask_list = Ask.objects.filter(pass_id=self._user)
        return ser.AskAbbrSerializer(instance=AskOperate._ask_list, many=True).data

    def undo_pass(self, ask_id):
        """老师不批准请假条"""
        try:
            self._ask_list = Ask.objects.get(id=ask_id)
            self._ask_list.status = "failed"
            self._ask_list.save()
            return True
        except Ask.DoesNotExist as ask_not_exist:
            print(ask_not_exist)
            return ask_not_exist

    def do_pass(self, ask_id, status):
        """老师通过请假条"""
        try:
            self._ask_list = Ask.objects.get(id=ask_id)

            self._ask_list.status = status
            self._ask_list.save()
            return True
        except Ask.DoesNotExist as ask_not_exist:
            print(ask_not_exist)
            return ask_not_exist


class AskToStudent(AskOperate):
    """
    学生->请假条
    """

    def views(self, audit_type):
        """学生查看请假条
        0表示审核中,1表示完成
        """
        # print("学生查看请假条,type =", audit_type)
        if not audit_type:
            AskOperate._ask_list = Ask.objects.filter(user_id=self._user)
        else:
            __status = ["passed", "failed"] if audit_type == "1" else [
                "draft", "first_audit", "scored_audit", "college_audit", "university_audit"]
            AskOperate._ask_list = Ask.objects.filter(user_id=self._user, status__in=__status)
        return ser.AskAbbrSerializer(instance=AskOperate._ask_list, many=True).data

    def submit(self, ask_id):
        """学生提交请假条"""
        try:
            self._ask_list = Ask.objects.get(id=ask_id)
            ser.AskAntiSerializer(Ask).update(self._ask_list, {'status': "first_audit"})
            return True
        except Ask.DoesNotExist as ask_not_exist:
            print(ask_not_exist)
            return ask_not_exist

    def modify(self, ask_id, validated_data):
        """学生修改请假条"""
        try:
            self._ask_list = Ask.objects.get(id=ask_id)
            ser.AskAntiSerializer(Ask).update(self._ask_list, validated_data)
            return True
        except Ask.DoesNotExist as ask_not_exist:
            print(ask_not_exist)
            return ask_not_exist

    def renew(self):
        """续假"""
        # TODO 续假不急
