from django.shortcuts import render

# Create your views here.


def check_login(func):  # 自定义登录验证装饰器
    def warpper(request, *args, **kwargs):
        is_login = request.session.get('is_login', False)
        print("是否登录", is_login)
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return render(request, "login.html")
    return warpper

