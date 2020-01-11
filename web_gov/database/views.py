from django.http import HttpResponse
import json
import pymysql
import sys
import os
from login.views import check_login
from multiprocessing import Process
import time
"""
在这个文件中，实现的是关于数据库的操作，
"""

MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'


@check_login
def get_all_table_names(request):
    """
    希望返回一个json数据格式, example:
    {
        'num': 2, #表示数量
        'names':['name1', 'name2'], # 一个list
    }
    """
    db = pymysql.connect(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD)
    curosr = db.cursor()
    SQL1 = "USE njudata;"
    curosr.execute(SQL1)
    SQL2 = "SHOW TABLES;"
    curosr.execute(SQL2)
    d = curosr.fetchall()
    print(d)
    data = dict({'num': 10, 'names': [s[0] for s in d]})
    curosr.close()
    db.close()
    return HttpResponse(json.dumps(data), content_type='application/json')


def file_to_db(name):
    (filename, extension) = os.path.splitext(name)
    print(filename, extension)
    if extension in ['.data', '.csv', '.db']:
        if extension == '.data':
            db = pymysql.connect(
                host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD)
            curosr = db.cursor()
            SQL1 = "USE njudata;"
            curosr.execute(SQL1)
            lens = 0
            with open('database/static/files/' + name, 'r') as f:
                for line in f.readlines():
                    lens = len(line.strip().split(","))
                    SQL_creat_table = "CREATE TABLE " + filename
                    SQL_creat_table += " (" + ",".join([
                        "col" + str(i) + " varchar(100)"
                        for i in range(1, lens + 1)
                    ]) + ");"
                    curosr.execute(SQL_creat_table)
                    db.commit()
                    break
            with open('database/static/files/' + name, 'r') as f:
                for line in f.readlines():
                    sline = line.strip().split(",")
                    if len(sline) < lens:
                        continue
                    sql = 'insert into ' + filename + "(" + ",".join(["col" + str(i) for i in range(1, 1 + lens)]) \
                          + ') values (' + ",".join(["%s" for i in range(lens)]) + ');'
                    curosr.execute(sql, sline)
                    db.commit()
            curosr.close()
            db.close()


@check_login
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
    if request.method == 'GET':
        print("获取数据", request.GET)
        classid = request.GET["classid"]
        db = pymysql.connect(
            host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD)
        curosr = db.cursor()
        SQL1 = "USE njudata;"
        curosr.execute(SQL1)
        SQL2 = "SHOW TABLES;"
        curosr.execute(SQL2)
        d = curosr.fetchall()
        all_sets = set([s[0] for s in d])
        print(all_sets)
        print(classid in all_sets)
        if classid in all_sets:
            SQL3 = "SELECT * FROM  {name} LIMIT 0,100;".format(name=classid)
            curosr.execute(SQL3)
            d = curosr.fetchall()
            data = [list(s) for s in d]
            return HttpResponse(
                json.dumps(data), content_type='application/json')


def get_table_content(name):
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
    db = pymysql.connect(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD)
    curosr = db.cursor()
    SQL1 = "USE njudata;"
    curosr.execute(SQL1)
    SQL3 = "SELECT * FROM  {name};".format(name=name)
    curosr.execute(SQL3)
    d = curosr.fetchall()
    data = [list(s) for s in d]
    return data


@check_login
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
    try:
        if request.method == 'POST':
            file_obj = request.FILES.get('file', None)
            print(file_obj.name)
            print(file_obj.size)
            with open('database/static/files/' + file_obj.name, 'wb') as f:
                for line in file_obj.chunks():
                    f.write(line)
            f.close()
            p = Process(target=file_to_db, args=(file_obj.name, ))
            p.start()
            # 收到的文件存在了files下面。接下来就是入库解析，
            data = dict()
            data['status'] = 1
            return HttpResponse(
                json.dumps(data), content_type='application/json')
    except:
        data = dict()
        data['status'] = 1
        return HttpResponse(json.dumps(data), content_type='application/json')


@check_login
def update_table_content(request):
    """
    暂时不需要
    :param request:
    :return:
    """
    return HttpResponse("Hello world ! ")
