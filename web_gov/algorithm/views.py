from login.views import check_login
from django.http import HttpResponse
import json
import pymysql
import sys
import os
from login.views import check_login
from multiprocessing import Process, Queue
import time
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
#from sklearn.neighbors import LocalOutlierFactor
from database.views import  get_table_content
from sklearn.model_selection import train_test_split
import numpy
import os
from django.shortcuts import render
from algorithm import  tsne
from algorithm.models import Running

from sklearn import metrics


def scores(target, y):
    prec = metrics.precision_score(target, y)
    recall = metrics.recall_score(target, y)
    f1 = metrics.f1_score(target, y)
    return prec, recall, f1


def LOF(dataset, index):
    data = get_table_content(dataset)
    model = LocalOutlierFactor(n_neighbors=4, contamination=0.01,  novelty=True)
    data = numpy.array(data)
    h, w = data.shape
    print(h, w)
    last_is_target = False
    if dataset in ['num3', 'num_n']:
        last_is_target = True
    All = None
    target = None
    for i in range(w):
        col = data[:, i]
        try:
            col = numpy.reshape(col.astype(numpy.float32), (-1, 1))
        except:
            le = preprocessing.LabelEncoder()
            le.fit(list(set(col)))
            col = le.transform(col)
            col = numpy.reshape(col.astype(numpy.float32), (-1, 1))
        if i == 0:
            All = col
        else:
            All = numpy.concatenate((All, col), -1)
    if last_is_target:
        target =All[:, -1].astype(numpy.int32)
        All = All[:, :-1]
    model.fit(All)
    job = Running.objects.get(create_time=index)
    job.status = 50
    job.save()
    y = model.predict(All)  # 若样本点正常，返回1，不正常，返回-1
    y[y == -1] = 0
    p, r, f1 = scores(target, y)
    with open(str(index), 'w') as f:
        f.write(str(p)+","+str(r)+","+str(f1)+'\n')
        f.write(str(dataset) + "," + "LOF" + "," + str(index))
    fig = tsne.tsne(All, y+1)
    fig.savefig('media/'+str(index)+'.png')
    job = Running.objects.get(create_time=index)
    job.status = 100
    job.save()


algorithm_set = {
    'LOF': LOF
}


@check_login
def run(request):
    data = dict()
    if request.method == 'POST':
        name = request.POST['classid']
        job = Running(dataset=request.POST['classid2'], status=0, algorithm=name)
        job.save()
        p = Process(target=algorithm_set[request.POST['classid2']], args=(name, job.create_time))
        p.start()
        data['status'] = 1
        return HttpResponse(json.dumps(data), content_type='application/json')


@check_login
def algorithm_names(request):
    data = dict()
    data['names'] = list(algorithm_set.keys())
    return HttpResponse(json.dumps(data), content_type='application/json')


@check_login
def running_jobs(request):
    data = [['algorithm', 'dataset', 'status', 'create_time']]
    jobs = Running.objects.all()
    for each in jobs:
        data.append([each.dataset, each.algorithm, str(each.status)+"%", each.create_time.__str__()])

    return HttpResponse(json.dumps(data), content_type='application/json')


@check_login
def show_details(request):
    data = request.GET.dict()
    print(data)
    time = data['time']
    context = {}
    with open(time, 'r') as f:
        lines = f.readlines()
        s = lines[0].strip().split(',')
        context['pre'] = s[0]
        context['recall'] = s[1]
        context['f1'] = s[2]
        s = lines[1].strip().split(',')
        context['dataset'] = s[0]
        context['algorithm'] = s[1]
        context['create_time'] = s[2]
    #data = dict()
    print(context)
    return render(request, "result_details.html", context=context)
    #return HttpResponse(json.dumps(data), content_type='application/json')

