'''
Audit模型和类冲突，曲线救国
'''
from .models import Audit

def audit(user_id,ask_unit,status,explain):
    '''
    设置audit
    '''
    return Audit(
        user_id=user_id,
        ask_id=ask_unit,
        status=status,
        explain=explain
        )
