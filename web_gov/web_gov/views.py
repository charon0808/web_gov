from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
import sys

from login.models import User
from login.views import check_login
import json


@check_login
def hello(request, name='index.html'):

    htmls = ['calendar.html', 'chart.html', 'file-manager.html', 'form.html', 'gallery.html', 'icon.html', 'index.html',
             'login.html', 'messages.html', 'submenu.html''submenu2.html', 'submenu3.html', 'table.html', 'tasks.html',
             'typography.html', 'ui.html', 'widgets.html', 'file_upload.html', '404.html', 'data_preview.html', 'algorithm_preview.html',
             "run_manage.html",
             "algorithm_go.html"]
    print(name, "=====================================================")
    if name in htmls:
        return render(request, name)
    else:
        return render(request, '404.html')


def login_user(request):
    print("LOGIN")
    if request.method == 'POST':
        print(request.POST)
        all_data = request.POST
        print(all_data)
        exist = User.objects.filter(username=all_data['username'], password=all_data['password']).first()
        print('EXIST', exist)
        if exist:
            request.session['is_login'] = True  # 设置session的随机字段值
            request.session['username'] = exist.username  # 设置uname字段为登录用户
            return redirect('/index.html')
        else:
            return HttpResponse("账户或密码错误")
    else:
        return render(request, 'login.html')


@check_login
def upload(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file', None)
        print(file_obj.name)
        print(file_obj.size)
        with open('media/' + file_obj.name, 'wb') as f:
            for line in file_obj.chunks():
                f.write(line)
        f.close()

        data = dict()
        data['status'] = 1
        return HttpResponse(json.dumps(data), content_type='application/json')

