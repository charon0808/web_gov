from django.http import HttpResponse
import json


"""
在这个文件中，实现的是关于数据库的操作，
"""


def get_all_table_names(request):
    """
    希望返回一个json数据格式, example:
    {
        'num': 2, #表示数量
        'names':['name1', 'name2'], # 一个list
    }
    """
    data = dict()
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_table_sample(request):
    """
    从get 参数里解析出想要查找的table name,返回最多五十个样例,example
    {
        'name': 'table1', #表示数量
        'samples':[
                    [2,3],
                    [3,4].
                    ], # 一个list数组，具体细节在补充
    }
    :param request:
    :return:
    """

    data = dict()
    return HttpResponse(json.dumps(data), content_type='application/json')


def write_table_content(request):
    """
        post格式，需要从中解析出文件名，文件类型，文件数据，然后写到database里面，表名就是文件名，不带后缀格式
        格式可能有csv,txt,db,等等
        {
            'name': 'table1', #表示数量
            'samples':[
                        [2,3],
                        [3,4].
                        ], # 一个list数组，具体细节在补充
        }
        :param request:
        :return:
        """
    done = True
    if done:
        return HttpResponse("1")
    else:
        return HttpResponse("0")


def update_table_content(request):
    """
    暂时不需要
    :param request:
    :return:
    """
    return HttpResponse("Hello world ! ")

