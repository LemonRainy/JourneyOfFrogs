import json
import time

from django.contrib.auth import authenticate, login

from django.http import HttpResponse
from django.shortcuts import render, redirect

from Frog import models

from Frog.models import User


# 修改专员个人信息
def changeInfo(request):
    if request.method == 'GET':
        expert_name = request.GET['expert_name']
        expert_tel = request.GET['expert_tel']
        expert_intro = request.GET['expert_intro']
        expert_gender = request.GET['expert_gender']
        expert_seniority = request.GET['expert_seniority']
        expert_company = request.GET['expert_company']
        expert_tag = request.GET['expert_tag']

        v = request.user.username
        models.Expert.objects.filter(email=v).update(tag=expert_tag,
                                                     company=expert_company,
                                                     gender=expert_gender,
                                                     seniority=expert_seniority,
                                                     name=expert_name,
                                                     telephone=expert_tel,
                                                     introduction=expert_intro)
        res = {'cool': True}
        return HttpResponse(json.dumps(res), content_type='application/json')


# 修改密码
def changePassword(request):
    if request.method == 'GET':

        old_password = request.GET['old_password']
        new_password = request.GET['new_password']
        new_password_confirm = request.GET['new_password_confirm']
        res = {}
        v = request.user.username

        if authenticate(username=v, password=old_password):
            if new_password == new_password_confirm:
                user = User.objects.get(username=v)
                user.set_password(new_password)
                user.save()
                res['cool'] = True
                res['res_message'] = '修改密码成功!'
            else:
                res['cool'] = False
                res['res_message'] = '两次新密码不一致!'
        else:
            res['cool'] = False
            res['res_message'] = '旧密码不正确!'

        return HttpResponse(json.dumps(res), content_type='application/json')


# 接受订单
def acceptOrder(request):
    if request.method == 'GET':
        order_id = request.GET['order_id']
        models.Order.objects.filter(orderID=order_id).update(state=1)
        res = {}
        res['cool'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


# 拒绝订单
def refuseOrder(request):
    if request.method == 'GET':
        order_id = request.GET['order_id']
        models.Order.objects.filter(orderID=order_id).update(state=-2)
        res = {}
        res['cool'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


# 取消订单
def cancelOrder(request):
    if request.method == 'GET':
        order_id = request.GET['order_id']
        models.Order.objects.filter(orderID=order_id).update(state=-1)
        res = {}
        res['cool'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


# 结束订单
def endOrder(request):
    if request.method == 'GET':
        order_id = request.GET['order_id']
        models.Order.objects.filter(orderID=order_id).update(state=2)
        res = {}
        res['cool'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


# 查看历史订单
def expertOrderList(request):
    v = request.user.username
    if v:
        orders = models.Order.objects.filter(expert_id=v).exclude(state__in=[0, 1]).order_by("-date")
        return render(request, '../templates/complete/expertOrderListPage.html', {'orders': orders})
    else:
        return redirect('/expert')


# 专员个人中心
def expert(request):
    if request.method == 'GET':
        expert = models.Expert.objects.get(email=request.user.username)
        if expert:
            return render(request, '../templates/complete/expertPage.html', {'expert': expert})

    elif request.method == 'POST':
        pass


# 服务订单
def orderHandling(request):
    v = request.user.username
    if v:
        orders = models.Order.objects.filter(expert_id=v, state__in=[0, 1]).order_by("-date")
        return render(request, '../templates/complete/orderHandlingPage.html', {'orders': orders})
    else:
        return redirect('/expert')


# 城市详情
def cityDetail(request):
    city_name = request.GET.get('cityName')
    city = models.City.objects.get(cityName=city_name)
    return render(request, '../templates/complete/city_detail.html', {'city': city})


# 景点详情
def spotDetail(request):
    spot_name = request.GET.get('spotName')
    spot = models.Spot.objects.get(spotName=spot_name)
    return render(request, '../templates/complete/spot_detail.html', {'spot': spot})


# 查看专员列表
def expertList(request):
    experts = models.Expert.objects.all()
    return render(request, '../templates/complete/expertList.html', {'experts': experts})
