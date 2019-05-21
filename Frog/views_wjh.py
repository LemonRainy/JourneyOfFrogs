import time

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Frog import models


def expertOrderList(request):
    return render(request, '../templates/expertOrderListPage.html')


def expert(request):
    # 输入的邮箱和密码
    email_input = "2973493373@qq.com"
    password = "123456"
    expert = models.Expert.objects.get(email=email_input, password=password)

    if expert:
        # 登录成功返回页面
        request.session['expert_email'] = expert.email
        return render(request, '../templates/expertPage.html', {'expert': expert})
    else:
        return HttpResponse("用户名或者密码错误")


def orderHandling(request):
    v = request.session.get('expert_email')
    if v:
        orders = models.Order.objects.filter(expert_id=v, state=0)


        return render(request, '../templates/orderHandlingPage.html', {'orders': orders})
    else:
        return redirect('/expert')
