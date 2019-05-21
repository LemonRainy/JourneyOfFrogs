from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

from Frog import models


def expertOrderList(request):
    return render(request, '../templates/expertOrderListPage.html')


def expert(request):
    # 输入的邮箱和密码
    email_input = "2973493373@qq.com"
    password = "123456"
    lines = models.Expert.objects.filter(email=email_input, password=password)
    if lines:
        # 登录成功返回页面
        return render(request, '../templates/expertPage.html')
    else:
        return HttpResponse("用户名或者密码错误")



def orderHandling(request):
    return render(request, '../templates/orderHandlingPage.html')
