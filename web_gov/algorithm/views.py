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
# from sklearn.neighbors import LocalOutlierFactor
from database.views import get_table_content
from sklearn.model_selection import train_test_split
import numpy
import os
from django.shortcuts import render
from algorithm import tsne
from algorithm.models import Running
from PyNomaly import loop
import pandas as pd
import copy

from sklearn import metrics


def scores(target, y):
    print(str(target), end="\n\n\n")
    print(str(y), end="\n\n\n")
    prec = metrics.precision_score(target, y)
    recall = metrics.recall_score(target, y)
    f1 = metrics.f1_score(target, y)
    return prec, recall, f1


def LOF(dataset, index):
    job = Running.objects.get(create_time=index)
    job.status = 50
    job.save()
    data = get_table_content(dataset)
    data_ori = copy.deepcopy(data)
    target = None if isinstance(data[0][-1], str) or dataset == "gov" else list(
        map(lambda x: x[-1], data))
    model = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
    data = [list(map(lambda x: float(x), d[:-1])) for d in data]
    pred = model.fit_predict(data)
    pred[pred == -1] = 0
    if not target is None:
        try:
            p, r, f1 = scores(target, pred)
        except Exception as e:
            p, r, f1 = 0, 0, 0
    else:
        p, r, f1 = 0, 0, 0
    filename = str(index).replace(" ", "_").replace(":", "_")
    out_pred_ID = []
    for i in range(len(pred)):
        if pred[i] == 0:
            out_pred_ID.append(data_ori[i][-1])
    print(str(out_pred_ID))
    with open(filename, 'w') as f:
        f.write(str(p) + "," + str(r) + "," + str(f1) + '\n')
        f.write(str(dataset) + "," + "LOF" + "," + str(index) + '\n')
        f.write(",".join(out_pred_ID))
        f.close()
    fig = tsne.tsne(data, pred + 1)
    fig.savefig('media/' + str(index) + '.png')
    job = Running.objects.get(create_time=index)
    job.status = 100
    job.save()


def LOOP(dataset, index):
    job = Running.objects.get(create_time=index)
    job.status = 10
    job.save()
    data = get_table_content(dataset)
    data_ori = copy.deepcopy(data)
    data = list(map(lambda x: list(map(float, x[:-1])), data))
    _data = copy.deepcopy(data)
    target = None if isinstance(data[0][-1], str) or dataset == "gov" else list(
        map(lambda x: x[-1], data))
    data = numpy.array(data)
    train_set = loop.LocalOutlierProbability(data, n_neighbors=20).fit()
    train_scores = train_set.local_outlier_probabilities
    job = Running.objects.get(create_time=index)
    job.status = 50
    job.save()
    threshold = 0.15
    pred = list(map(lambda x: 1 if x < threshold else 0, train_scores))
    # print(pred)
    if not target is None:
        p, r, f1 = scores(target, pred)
    else:
        p, r, f1 = 0, 0, 0
    filename = str(index).replace(" ", "_").replace(":", "_")
    out_pred_ID = []
    for i in range(len(pred)):
        if pred[i] == 0:
            out_pred_ID.append(data_ori[i][-1])
    print(str(out_pred_ID))
    with open(filename, 'w') as f:
        f.write(str(p) + "," + str(r) + "," + str(f1) + '\n')
        f.write(str(dataset) + "," + "LOOP" + "," + str(index) + '\n')
        f.write(",".join(out_pred_ID))
        f.close()
    fig = tsne.tsne(_data, numpy.array(pred) + 1)
    fig.savefig('media/' + str(index) + '.png')
    job = Running.objects.get(create_time=index)
    job.status = 100
    job.save()


algorithm_set = {'LOF': LOF, 'LOOP': LOOP}


@check_login
def run(request):
    data = dict()
    if request.method == 'POST':
        name = request.POST['classid']
        job = Running(
            dataset=request.POST['classid2'], status=0, algorithm=name)
        job.save()
        p = Process(
            target=algorithm_set[request.POST['classid2']],
            args=(name, job.create_time))
        p.start()
        print(str(p))
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
        data.append([
            each.dataset, each.algorithm,
            str(each.status) + "%",
            each.create_time.__str__().replace(" ", "_").replace(":", "_")
        ])

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
        if len(lines) > 2:
            s = lines[2].strip().split(',')
            context['outlier_ID'] = "\t".join(s)
    # data = dict()
    print(context)
    return render(request, "result_details.html", context=context)
    # return HttpResponse(json.dumps(data), content_type='application/json')
