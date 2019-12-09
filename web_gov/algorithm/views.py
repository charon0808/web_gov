from login.views import check_login
from django.http import HttpResponse
import json
import pymysql
import sys
import os
from login.views import check_login
from multiprocessing import Process
import time
from sklearn.neighbors import LocalOutlierFactor
#from sklearn.neighbors import LocalOutlierFactor
from database.views import  get_table_content
import numpy


def LOF(dataset):
    data = get_table_content(dataset)
    model = LocalOutlierFactor(n_neighbors=4, contamination=0.1,  novelty=True)
    model.fit(numpy.array(data)[:, 0:2])
    y = model._predict(numpy.array(data)[:, 0:2])  # 若样本点正常，返回1，不正常，返回-1
    print(y)
    pass


algorithm_set = {
    'LOF': LOF
}


@check_login
def run(request):
    if request.method == 'POST':
        name = request.POST['classid']
        p = Process(target=algorithm_set[request.POST['classid2']], args=(name,))
        p.start()
        print("获取数据", request.POST)
    return HttpResponse("OK")


@check_login
def algorithm_names(request):
    data = dict()
    data['names'] = list(algorithm_set.keys())
    return HttpResponse(json.dumps(data), content_type='application/json')
