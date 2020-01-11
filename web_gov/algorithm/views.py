from login.views import check_login
from django.http import HttpResponse
import json
import pymysql
import sys
import os
from login.views import check_login
from multiprocessing import Process, Queue
import time
import sklearn
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
from PyNomaly import loop
from scipy.spatial.distance import pdist, squareform

def scores(target, y):
    prec = metrics.precision_score(target, y)
    recall = metrics.recall_score(target, y)
    f1 = metrics.f1_score(target, y)
    return prec, recall, f1

def dist(X):
    sq_dists = pdist(X)
    mat_sq_dists = squareform(sq_dists)
    return mat_sq_dists

def c_dist(X):
    length  =len(X)
    dis = numpy.zeros((length,length))
    for i in range(length-1):
        for j in range(i+1,length):
            dis[i,j]=dis[j,i] = sum(X[i]==X[j])
    return dis

def pre_data(database):
    data = get_table_content(database)
    head = data[0]
    data = numpy.array(data[1:])
    h, w = data.shape
    last_is_target = False
    target = None
    if head[-1].split(':')[-1]=='T':
        last_is_target = True
    n_data = None
    c_data = None
    for i in range(w):
        col = data[:, i]
        if head[i].split(':')[-1]=='C':
            col = numpy.reshape(col, (-1, 1))
            if c_data is None:
                c_data = col
            else:
                c_data = numpy.concatenate((c_data, col), -1)
        else:
            col = numpy.reshape(col.astype(numpy.float32), (-1, 1))
            col = sklearn.preprocessing.minmax_scale(col)
            sklearn.preprocessing.scale(col, axis=0, with_mean=True,with_std=True,copy=True)  
            if n_data is None:
                n_data = col
            else:
                n_data = numpy.concatenate((n_data, col), -1)
    if last_is_target:
        target =n_data[:,-1].astype(numpy.int32)
        n_data = n_data[:,:-1]
    return n_data,c_data,target
def LOOP(database,index):
    n_data,c_data,target = pre_data(database)
    job = Running.objects.get(create_time=index)
    job.status = 50
    job.save()
    m = loop.LocalOutlierProbability(n_data).fit()
    score = m.local_outlier_probabilities
    num = int(len(n_data)*0.1)
    ind = numpy.argpartition(score, -num)[-num:]
    y = numpy.ones(len(n_data))
    y[ind] = 0
    if target is not None:
        p, r, f1 = scores(target, y)
    else :
        p,r,f1=0,0,0
    with open(str(index), 'w') as f:
        f.write(str(p)+","+str(r)+","+str(f1)+'\n')
        f.write(str(database) + "," + "LOOP" + "," + str(index))
    fig = tsne.tsne(n_data, y+1)
    #fig2 = tsne.tsne(n_data, 1-target)
    fig.savefig('media/'+str(index)+'.png')
    job = Running.objects.get(create_time=index)
    job.status = 100
    job.save()

def LOF(dataset, index):
    data = get_table_content(dataset)
    model = LocalOutlierFactor(n_neighbors=20,metric='precomputed', contamination=0.1,  novelty=False)
    n_data,c_data,target = pre_data(dataset)
    X = dist(n_data)
    X_2 = c_dist(c_data)
    X = sklearn.preprocessing.minmax_scale(X)
    sklearn.preprocessing.scale(X, axis=0, with_mean=True,with_std=True,copy=True) 
    X_2 = sklearn.preprocessing.minmax_scale(X_2)
    sklearn.preprocessing.scale(X_2, axis=0, with_mean=True,with_std=True,copy=True)
    alpha = 0
    y = model.fit_predict(X+alpha*X_2)
    y[y == -1] = 0
    job = Running.objects.get(create_time=index)
    job.status = 50
    job.save()
    # 若样本点正常，返回1，不正常，返回-1
    if target is not None:
        p, r, f1 = scores(target, y)
    else :
        p,r,f1=0,0,0
    with open(str(index), 'w') as f:
        f.write(str(p)+","+str(r)+","+str(f1)+'\n')
        f.write(str(dataset) + "," + "LOF" + "," + str(index))
    fig = tsne.tsne(n_data, y+1)
    #fig2 = tsne.tsne(n_data, 1-target)
    fig.savefig('media/'+str(index)+'.png')
    job = Running.objects.get(create_time=index)
    job.status = 100
    job.save()


algorithm_set = {
    'LOF': LOF,
    'LOOP':LOOP
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

