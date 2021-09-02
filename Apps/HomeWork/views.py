'''
Author: 邹洋
Date: 2021-09-02 14:36:25
Email: 2810201146@qq.com
LastEditors:  
LastEditTime: 2021-09-02 14:57:16
Description: 
'''

from cool.views import CoolAPIException, CoolBFFAPIView, ErrorCode, ViewSite
from django.utils.translation import gettext_lazy as _

# Create your views here.

site = ViewSite(name='SchoolInformation', app_name='SchoolInformation')

@site
class HomeWork(ModelViewSet):
    name = _('XXX')
   
    def get_context(self, request, *args, **kwargs):
        data = []
        return data
    # class Meta:
    #     param_fields = (
    #         ('username', fields.CharField(label=_('用户名'), default=None)),
    #     )



urls = site.urls
urlpatterns = site.urlpatterns
