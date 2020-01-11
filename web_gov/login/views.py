from django.shortcuts import render,redirect

# Create your views here.


def check_login(func):  # 自定义登录验证装饰器
    def warpper(request, *args, **kwargs):
        is_login = request.session.get('is_login', True)
        if is_login:
            return func(request, *args, **kwargs)
        else:
            response = redirect('/login.html')
            return response
            #return render(request, "login.html")
    return warpper

