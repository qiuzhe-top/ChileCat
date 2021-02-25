'''
APIView:restframework框架
JsonResponse:返回json应答(默认为httpresponse)
paginator:分页器
objectdoesnotexist:查询不存在(get)抛出的异常
'''
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
# import json
from . import models, ser
from .models import TypeParent


# Create your views here.


class Info(APIView):
    '''
    信息
    http://127.0.0.1:8000/api/career/info
    page:10 per
    '''

    def get(self, request):
        """
        处理get请求
        """
        redic = request.GET
        text_id = redic.get('id', -1)
        data = {}
        if text_id != -1:
            ret = {
                'id': 0,
                'title': "on title",
                'introduction': "on introduction",
                'body_text': "on more details",
                'creation_time': "0000.00.00"
            }
            try:
                ret_info = models.Career.objects.get(id=text_id)
            except ObjectDoesNotExist as do_not_find:
                print("no this text", do_not_find)
                error_message = {'info': "no id = " + text_id + " text!"}
                return JsonResponse(error_message)
            ret['id'] = ret_info.id
            ret['title'] = ret_info.title
            ret['introduction'] = ret_info.note
            ret['body_text'] = ret_info.text
            ret['creation_time'] = ret_info.release_time
            return JsonResponse(ret)
        else:  # id不存在,查询all,并根据page返回第几页
            rets = {
                'page': -1,
                'max_page': -1,
                'list': []
            }
            ret_page = int(redic.get('page', -1))
            if ret_page == -1:
                ret = {'message': "on id and no page."}
                return JsonResponse(ret)
            if ret_page <= 0:
                ret_page = 1
            ret = {
                'id': "-1",
                'title': "no title",
                'body_text': "none",
                'creation_time': "0000.00.00",
            }
            rets['page'] = ret_page
            text_list = models.Career.objects.all()
            paginator = Paginator(text_list, 10)  # 每页显示十项
            rets['max_page'] = paginator.num_pages
            if rets['max_page'] == 0:
                return JsonResponse({'info': "no data."})
            for i in paginator.page(ret_page):
                ret['id'] = i.id
                ret['title'] = i.title
                ret['body_text'] = i.note
                ret['creation_time'] = i.release_time
                rets['list'].append(ret)
            data['code'] = 2000
            data['message'] = '执行成功'
            data['data'] = rets
            return JsonResponse(data)


# 获取新闻导航
def press_navigation():
    """获取新闻导航"""
    ret = {}
    vx_news_grade = '微信新闻导航'
    try:
        car = TypeParent.objects.get(title=vx_news_grade)
    except TypeParent.DoesNotExist:
        ret['code'] = 4000
        ret['data'] = "没有数据"
        return ret
    type_child = car.typechild_set.all()
    type_child_ser = ser.TypeChildSerializer(instance=type_child, many=True).data
    # print(type_child_ser)
    ret['code'] = 2000
    ret['data'] = type_child_ser
    return ret


# 获取分类下的新闻列表
def news_list(chilid):
    """获取分类下的新闻列表"""
    ret = {}
    child_list = models.Career.objects.filter(classify=chilid)
    child_ser = ser.CareerListSerializer(instance=child_list, many=True).data
    # print(child_ser)
    ret['code'] = 2000
    ret['data'] = child_ser
    return ret


def news_details(carid):
    """获取新闻详情"""
    ret = {}
    try:
        car = models.Career.objects.get(id=carid)
    except ObjectDoesNotExist:
        ret['code'] = 5000
        ret['message'] = "当前文章不存在"
        return ret
    car_ser = ser.CareerSerializer(instance=car, many=False).data
    # print("car_ser", car_ser)
    ret['code'] = 2000
    ret['data'] = car_ser
    return ret


class NewsCat(APIView):
    """新闻"""

    def get(self, request):
        """获取新闻"""
        career_id = request.GET.get('id', -1)
        career_type = request.GET.get('type', -1)
        if career_id != -1:
            ret = news_details(career_id)
        elif career_type != -1:
            ret = news_list(career_type)
        else:
            ret = press_navigation()
        # print(ret)
        return JsonResponse(ret)

    def post(self, request):
        """提交新闻"""
        ret = {}
        data = request.data
        # lists = models.Career.objects.all()[:3]
        news = ser.CareerForSerializer(data=data)
        ret['code'] = news.is_valid()
        news.save()
        # print(s.is_valid())
        # s.update()
        ret['message'] = 'message'
        ret['data'] = 'data'
        return JsonResponse(ret)
