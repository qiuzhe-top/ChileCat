
from rest_framework.pagination import PageNumberPagination


class RecordQueryrPagination(PageNumberPagination):
    # 每页显示多少个
    page_size = 30
    # 默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数
    page_size_query_param = "size"
    # 最大页数不超过10
    # max_page_size = 10
    # 获取页码数的
    page_query_param = "page"
