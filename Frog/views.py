from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from Frog import models
from email.mime.text import MIMEText  # 用于发送邮件的类
import json


# Create your views here.


def index(request):
    return redirect('/index')


def login_view(request):
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
    if request.method == "POST":
        print(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')
        gender = request.POST.get('sex')
        type = request.POST.get('type')

        user = models.User.objects.create_user(username=email,
                                               password=password,
                                               telephone=telephone,
                                               name=name,
                                               gender=gender,
                                               type=type)

        if type == '订制专员':
            # 添加用户到expert表
            models.Expert.objects.create(email=email, name=name, gender=gender, telephone=telephone)
            return redirect('/index')
        if type == '普通用户':
            # 添加用户到member表
            models.Member.objects.create(email=email, name=name, gender=gender, telephone=telephone)
        login(request, user)

    if request.user.is_authenticated:
        return redirect('/index')
    return render(request, "../templates/complete/registerPage.html")


def modifyPassword(request):
    if request.method == "POST":
        # 输入的密码
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        code = request.POST.get('code')

        res = {}
        email = request.session.get('email')
        oldPassword = models.Expert.objects.get(email=email).password
        if password == oldPassword:
            if password1 == password2:
                models.Expert.objects.filter(email=email).update(password=password1)
                res['cool'] = True
                res['res_message'] = '修改成功!'
            else:
                res['cool'] = False
                res['res_message'] = '输入新密码不一致!'
        else:
            res['cool'] = False
            res['res_message'] = '原始密码错误!'

        return HttpResponse(json.dumps(res), content_type='application/json')


def logoff(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/index')
    else:
        return redirect('/index')


def log(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = authenticate(username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            if user.type == '订制专员':
                return redirect('/expert')
            return redirect('/index')
    return render(request, "../templates/complete/loginPage.html")


def indexpage(request):
    if request.user.is_authenticated:
        if request.user.type == '订制专员':
            return redirect('/expert')
    return render(request, "../templates/complete/indexPage.html")


def customize(requesrt):
    return render(requesrt, "../templates/complete/customizePage.html")


def user(request):
    return render(request, "../templates/complete/userPage.html")


def historyOrder(request):
    email = request.session.get('email')
    if email:
        orders = models.Order.objects.filter(expert_id=email)
        return render(request, '../templates/orderListPage.html', {'orders': orders})
    else:
        return redirect('/personal')
