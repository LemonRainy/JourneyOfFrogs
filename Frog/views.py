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
        location = request.POST.get('location')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')
        gender = request.POST.get('sex')
        type = request.POST.get('type')
        print([name, email, location, telephone, password, gender, type])
        user = models.User.objects.create_user(password=password,
                                               location=location,
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
            models.Member.objects.create(email=email, location=location, name=name, gender=gender, telephone=telephone)
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
            searchSpot = request.POST.get('searchSpot')
            searchPeopleNumber = request.POST.get('searchPeopleNumber')
            searchDays = request.POST.get('searchDays')
            searchBudget = request.POST.get('searchBudget')
            strategys=[];
            # searchSortord = request.POST.get('searchSortord')
            # cursor.execute(
            #     'select * from Frog_city, Frog_strategy, Frog_cityincluded where cityName=cityName_id and strategyId=strategyId_id and cityName=\'{}\''.format(searchCity));
            # strategyList=dictfetchall(cursor);
            # print(strategyList);


            return render(request, "../templates/strategyListPage.html", {'strategyList': strategys,
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

                print('符合标准的：');
                print(strategyIds);
                # 找到了所有符合标准的攻略Id攻略
                for strategyId in strategyIds:
                    cursor.execute(
                        'select strategyTitle, budget, name, days, peopleNumber, content, count(Frog_digg.useremail_id) as likeNumber '
                        'from Frog_strategy, Frog_member, Frog_digg '
                        'where email=memberEmail_id and strategyId=strategy_id and strategyId=\'{}\''
                        'group by Frog_digg.strategy_id'.format(strategyId));
                    strategyList = dictfetchall(cursor);
                print('符合标准的：');
                print(strategyList);

            else:
                cursor.execute(
                    'select strategyTitle, budget, name, days, peopleNumber, content, count(Frog_digg.useremail_id) as likeNumber '
                        'from Frog_strategy, Frog_member, Frog_digg '
                        'where email=memberEmail_id and strategyId=strategy_id group by Frog_digg.strategy_id');
                strategyList = dictfetchall(cursor);
                print(strategyList);

            return render(request, "../templates/strategyListPage.html", {'strategyList': strategyList
                                                                          })
    if request.method=="GET":
        cursor = connection.cursor();
        cursor.execute(
            'select strategyTitle, budget, name, days, peopleNumber, content, count(Frog_digg.useremail_id) as likeNumber '
                        'from Frog_strategy, Frog_member, Frog_digg '
                        'where email=memberEmail_id and strategyId=strategy_id group by Frog_digg.strategy_id');
        strategys = dictfetchall(cursor);
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