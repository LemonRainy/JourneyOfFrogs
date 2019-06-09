import time
from django.core import serializers
from django.shortcuts import render, redirect

from Frog import models


# 私人定制
def customize(request):
    if request.method == "POST":
        travelNum = request.POST.get('travelNum')
        childNum = request.POST.get('childNum')
        departureCity = request.POST.get('departureCity')
        destinationCity = request.POST.get('destinationCity')
        departureTime = request.POST.get('departureTime')
        destinationTime = request.POST.get('destinationTime')
        expertName = request.POST.get('expertName')
        intent = request.POST.get('note')
        # expertEmail = models.Expert.objects.filter(name=expertName).values_list('email', flat=True)
        expert = models.Expert.objects.filter(name=expertName)
        member = models.Member.objects.filter(email=request.user.username)
        print('意愿信息：', intent)


        # 生成唯一订单号
        year = time.localtime()[0]
        month = time.localtime()[1]
        day = time.localtime()[2]
        hour = time.localtime()[3]
        minute = time.localtime()[4]
        second = time.localtime()[5]
        orderID = 'QWLV' + str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second)

        order = models.Order.objects.create(
            member=member[0],
            expert=expert[0],
            state=0,
            date=time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())),
            intent=intent,
            travelNum=travelNum,
            childNum=childNum,
            departureCity=departureCity,
            destinationCity=destinationCity,
            departureTime=departureTime,
            destinationTime=destinationTime,
            orderID=orderID)

        return redirect('/index')
    experts = models.Expert.objects.values_list('name', flat=True)
    return render(request, "../templates/complete/customizePage.html", locals())


# 私人定制列表
def orderList(request):
    if request.method == "GET":
        orderlist = models.Order.objects.filter(member_id=request.user.username)
        print(request.user.username)
        print(orderlist)
        return render(request, "../templates/complete/orderList.html", locals())
    return redirect('/orderDetail')


# 订单详细信息
def orderDetail(request, orderID):
    id = orderID[1:-1]
    if request.method == "GET":
        orderList = models.Order.objects.filter(orderID=id)
        order = orderList[0]
        comment = "已评价"
        state = "订单正在等待服务"
        if order.state == 2:
            state = "订单已完成"
        if order.state == -1:
            state = "订单已取消"
        if order.state == -2:
            state = "订单已拒绝"

        if order.comment == "":
            comment = "未评价"

        if order.mark == "":
            order.mark = 0
        return render(request, "../templates/complete/orderDetail.html", locals())

    # POST
    orderLists = models.Order.objects.filter(orderID=id)
    totalnum = request.POST.get("totalnum")
    if totalnum == "0":
        totalnum = None
    models.Order.objects.filter(orderID=id).update(comment=request.POST.get("comment"),
                                                   mark=totalnum)
    orders = models.Order.objects.filter(expert_id=orderLists[0].expert.email)
    sum = 0
    num = 0
    for order in orders:
        if order.mark:
            sum += order.mark
            num += 1
    if num is not 0:
        models.Expert.objects.filter(email=orderLists[0].expert.email).update(mark=float(sum / num))
    return redirect('/index')
