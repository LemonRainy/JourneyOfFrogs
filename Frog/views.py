from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from Frog import models
from django.core.mail import send_mail, send_mass_mail  # 用于发送邮件的类
import json
from django.conf import settings
from django.db import connection
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
        print([name, email, telephone, password, gender, type])
        user = models.User.objects.create_user(password=password,
                                               telephone=telephone,
                                               username=email,
                                               name=name,
                                               gender=gender,
                                               type=type)

        if type == '订制专员':
            # 添加用户到expert表
            models.Expert.objects.create(email=email, name=name, gender=gender, telephone=telephone)
            # return redirect('/index')
        if type == '普通用户':
            # 添加用户到member表
            models.Member.objects.create(email=email, name=name, gender=gender, telephone=telephone)
        login(request, user)

    if request.user.is_authenticated:
        if models.User.objects.get(username=request.user).type == "定制专员":
            return redirect('/expert')
        return redirect('/index')
    return render(request, "../templates/complete/registerPage.html")


def update(request):
    if request.method == "POST":
        # 输入的密码
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(password,password2,password1)

        email = request.user.username
        if authenticate(username=email, password=password):
            if password1 == password2:
                user = models.User.objects.get(username=email)
                user.set_password(password1)
                user.save()
                return redirect('/log')
    return render(request, "../templates/complete/updatePage.html")

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

    if request.method == "POST":
        # print(request.POST)
        # searchContent = request.POST.get('searchContent')
        # if searchContent:
        #     strategys = models.Strategy.objects.filter(strategyTitle__contains=searchContent)
        #     print(strategys)
        return redirect('/strategyList')
    return render(request, "../templates/complete/indexPage.html")

def user(request):
    return render(request, "../templates/complete/userPage.html")


def code(request):
    if request.method == "GET":
        print("get method")
        title = "青蛙旅行验证码"
        msg = "验证码："+ str(request.GET.get('code'))
        email_from = settings.EMAIL_HOST_USER
        reciever = request.GET.get('email')
        # 发送邮件
        print(reciever, msg)
        send_mail(title, str(msg), email_from, [reciever])

        return HttpResponse("邮件已发送！")

#查看历史攻略
def personal(request):
    email = request.user.username
    print("查看" + email)
    if email:
        strategies = models.Strategy.objects.filter(memberEmail=email)

        return render(request, '../templates/complete/personalPage.html', {'strategies': strategies})
    else:
        return render(request, "../templates/complete/personalPage.html")

    return render(request, "../templates/complete/personalPage.html")

def filterStrategy(request):
    if request.method== "POST":
        if request.POST.get('filterOrSearch'):
            # 筛选攻略
            print(request.POST)
            searchPeopleNumber = request.POST.get('searchPeopleNumber')
            searchDays = request.POST.get('searchDays')
            searchBudget = request.POST.get('searchBudget')
            filteredStrategys=[];
            strategys=[];
            cursor = connection.cursor();

            if request.session['strategyIdsToFilter']:
                strategyIdsToFilter=request.session['strategyIdsToFilter'];
                for one in strategyIdsToFilter:
                    cursor.execute(
                        'select strategyTitle, budget, name, days, peopleNumber, content, diggNumber, createDate from Frog_strategy, Frog_member where email=memberEmail_id and strategyId=\'{}\''.format(
                            one));
                    strategy = dictfetchall(cursor);
                    strategys += strategy;
                print("需要筛选的攻略：")
                print(strategys);
                if searchPeopleNumber and searchDays and searchBudget:
                    for one in strategys:
                        if one.get('peopleNumber')==searchPeopleNumber and one.get('days')==searchDays and one.get('budget')==searchBudget:
                            print("均符合")
                            if one not in filteredStrategys:
                                filteredStrategys+=one;
                    print("筛选后的攻略")
                    print(filteredStrategys)
                    print(" 人数，天数和预算都不空")

                if searchPeopleNumber and searchDays:
                    print(" 人数，天数都不空")

                if searchPeopleNumber and searchBudget:
                    print(" 人数，预算都不空")

                if searchDays and searchBudget:
                    print(" 天数,预算都不空")

                if searchPeopleNumber:
                    print(" 人数不空")

                if searchDays:
                    print(" 天数不空")

                if searchBudget:
                    print(" 预算不空")


                # print(strategyIdsToFilter)

            return render(request, "../templates/strategyListPage.html", {'strategyList': filteredStrategys,
                                                                          })
        else:
            # 搜索功能
            searchKeywords = request.POST.get('searchKeywords')
            cursor = connection.cursor();
            strategyList=[];

            if searchKeywords:
                # 搜索关键词：景点、城市、用户名称或攻略名
                strategyIds=[];
                # 景点
                cursor.execute(
                    'select strategyId from Frog_strategy, Frog_spotincluded where strategyId_id=strategyId and spotName_id=\'{}\''.format(
                        searchKeywords));
                dictCursor = dictfetchall(cursor);
                if dictCursor:
                    for one in dictCursor:
                        if one.get('strategyId') not in strategyIds:
                            strategyIds.append(one.get('strategyId'));

                # 城市
                cursor.execute(
                               'select strategyId from Frog_strategy, Frog_cityincluded where strategyId_id=strategyId and cityName_id=\'{}\''.format(searchKeywords));
                dictCursor = dictfetchall(cursor);
                if dictCursor:
                    for one in dictCursor:
                        if one.get('strategyId') not in strategyIds:
                            strategyIds.append(one.get('strategyId'));

                # 用户名
                cursor.execute(
                    'select strategyId from Frog_strategy, Frog_member where memberEmail_id=email and name=\'{}\''.format(searchKeywords));
                dictCursor = dictfetchall(cursor);
                print("用户名搜索");
                print(dictCursor);
                if dictCursor:
                    for one in dictCursor:
                        if one.get('strategyId') not in strategyIds:
                            strategyIds.append(one.get('strategyId'));

                #攻略标题
                cursor.execute(
                    'select strategyId from Frog_strategy where strategyTitle=\'{}\''.format(searchKeywords));
                dictCursor= dictfetchall(cursor);
                if dictCursor:
                    for one in dictCursor:
                        if one.get('strategyId') not in strategyIds:
                            strategyIds.append(one.get('strategyId'));

                print('符合标准的strategyIds：');
                print(strategyIds);
                # 找到了所有符合标准的攻略Id攻略
                for strategyId in strategyIds:
                    cursor.execute(
                        'select strategyTitle, budget, name, days, peopleNumber, content, diggNumber, createDate from Frog_strategy, Frog_member where email=memberEmail_id and strategyId=\'{}\''.format(strategyId));
                    strategy = dictfetchall(cursor);
                    strategyList += strategy;
                print('符合标准的strategyList：');
                print(strategyList);

            else:
                cursor.execute(
                    'select strategyTitle, budget, name, days, peopleNumber, content, diggNumber, createDate from Frog_strategy, Frog_member where email=memberEmail_id');
                strategyList = dictfetchall(cursor);
                print(strategyList);

            request.session['strategyIdsToFilter'] = strategyIds;
            return render(request, "../templates/strategyListPage.html", {'strategyList': strategyList
                                                                          })
    if request.method=="GET":
        cursor = connection.cursor();
        cursor.execute(
            'select strategyTitle, budget, name, days, peopleNumber, content, diggNumber, createDate from Frog_strategy, Frog_member where email=memberEmail_id');
        strategys = dictfetchall(cursor);
        print(strategys);
        return render(request, "../templates/strategyListPage.html", {'strategyList':strategys})

def dictfetchall(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    ]

def enterUserPage(request):
    return render(request,"../templates/userPage.html")