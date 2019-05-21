from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from Frog import models
from email.mime.text import MIMEText#用于发送邮件的类
# Create your views here.


def index(request):
    return render(request, '../templates/index.html')

def login(request):
    if request.method == "POST":
        # 输入的邮箱和密码
        email = request.POST.get('email')
        password = request.POST.get('password')
        member = models.Member.objects.get(email=email, password=password)

        if member:
            # 登录成功返回页面
            request.session['member_email'] = member.email
            return render(request, '../templates/index.html', {'member': member})
        else:
            return HttpResponse("用户名或密码错误")

def register(request):
    pass

def modifyPassword(request):
    if request.method == "POST":
        # 输入的密码
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        code = request.POST.get('code')

        if password1 == password2:
            user = models.User.objects.get(email=email, password=password)
                if code == token:
                if user:
                    # 登录成功返回页面
                    return HttpResponse("修改成功")
                else:
                    return HttpResponse("原始密码错误")

        else:
            return HttpResponse("请两次输入相同密码!")






def historyOrder(request):
    pass
