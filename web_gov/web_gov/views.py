from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
import sys

from login.models import User
import json


def check_login(func):  # 自定义登录验证装饰器
    def warpper(request, *args, **kwargs):


        is_login = request.session.get('is_login', False)
        print("是否登录",is_login)
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return render(request, "login.html")
    return warpper


@check_login
def hello(request, name='index.html'):

    #name = request.GET.get('name').split('/')[-1]

    htmls = ['calendar.html', 'chart.html', 'file-manager.html', 'form.html', 'gallery.html', 'icon.html', 'index.html',
             'login.html', 'messages.html', 'submenu.html''submenu2.html', 'submenu3.html', 'table.html', 'tasks.html',
             'typography.html', 'ui.html', 'widgets.html', 'file_upload.html', '404.html', 'data_preview.html', 'algorithm_preview.html',
             "algorithm_go.html"]
    if name in htmls:
        return render(request, name)
    else:
        return render(request, '404.html')

@check_login
def algorithm_names(request):
    data = dict()
    data['names'] = ['name1', 'name2']
    return HttpResponse(json.dumps(data), content_type='application/json')

@check_login
def run(request):
    print(request.POST)
    return HttpResponse('ok')

def login_user(request):
    print("LOGIN")
    if request.method == 'POST':
        print(request.POST)
        #form = LoginForm(request.POST)
        #print(form)
        all_data = request.POST
        if True:#form.is_valid():
            #all_data = form.clean()  # 获取post数据，例如 {'username': u'yang1', 'password': 111}
            #print(all_data)
            #exist =True
            exist = User.objects.filter(username=all_data['username'], password=all_data['password']).first()
            print('EXIST', exist)
            if exist:
                request.session['is_login'] = True  # 设置session的随机字段值
                request.session['username'] = exist.username  # 设置uname字段为登录用户
                return redirect('/index.html')
            else:
                return HttpResponse("账户或密码错误")
    return render(request, 'login.html')


def upload(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file', None)
        print(file_obj.name)
        print(file_obj.size)
        with open('static/media/' + file_obj.name, 'wb') as f:
            for line in file_obj.chunks():
                f.write(line)
        f.close()

        data = dict()
        data['status'] = 1
        return HttpResponse(json.dumps(data), content_type='application/json')

