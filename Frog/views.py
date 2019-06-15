from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from Frog import models
from django.core.mail import send_mail, send_mass_mail  # 用于发送邮件的类
import json
from django.conf import settings
from django.db import connection
# Create your views here.


# def index(request):
#     return redirect('/index')



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
                                               telephone=telephone,
                                               username=email,
                                               name=name,
                                               gender=gender,
                                               type=type)

        if type == '订制专员':
            # 添加用户到expert表
            models.Expert.objects.create(email=email, name=name, gender=gender, telephone=telephone, location=location)
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
        # 搜索功能
        searchContentIndex=request.POST.get('searchContentIndex')
        request.session['searchKeywords']=searchContentIndex;
        return redirect("/strategyList")
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
        member = models.Member.objects.get(email=email)
        return render(request, '../templates/complete/personalPage.html', {'strategies': strategies,
                                                                           'member': member,
                                                                           })
    else:
        return render(request, "../templates/complete/personalPage.html")

    # return render(request, "../templates/complete/personalPage.html")

# 筛选和搜索攻略
def strategyList(request):
    if request.method== "POST":
        if request.POST.get('filterOrSearch'):
            # 筛选攻略
            print(request.POST)
            searchKeywords=request.session['searchKeywords'];
            searchPeopleNumber = request.POST.get('searchPeopleNumber')
            searchDays = request.POST.get('searchDays')
            searchBudget = request.POST.get('searchBudget')
            filteredStrategys=[];
            strategys=[];
            cursor = connection.cursor();
            for one in request.session['strategyIdsToFilter']:
                print("request.session['strategyIdsToFilter']:"+str(one))

            if request.session['strategyIdsToFilter']!='':
                strategyIdsToFilter=request.session['strategyIdsToFilter'];
                print(strategyIdsToFilter);
                for one in strategyIdsToFilter:
                    cursor.execute(
                        'select strategyTitle, budget, name, days, peopleNumber, content, diggNumber, createDate, strategyId,coverUrl from Frog_strategy, Frog_member where email=memberEmail_id and strategyId=\'{}\''.format(
                            one));
                    strategy = dictfetchall(cursor);
                    strategys += strategy;
                print("需要筛选的攻略：")
                print(strategys);

            else:
                cursor.execute('select strategyTitle, budget, name, days, peopleNumber, content, diggNumber, createDate, strategyId,coverUrl from Frog_strategy, Frog_member where email=memberEmail_id')
                strategys=dictfetchall(cursor);
                print(strategys)

                print("需要筛选的攻略：")
                print(strategys);

            if searchPeopleNumber and searchDays and searchBudget:
                    for one in strategys:
                        if one.get('peopleNumber') == int(searchPeopleNumber) and one.get('days') == int(searchDays) and one.get('budget') <= int(searchBudget):
                            # print("均符合")
                            if one not in filteredStrategys:
                                filteredStrategys.append(one);
                    # print(" 人数，天数和预算都不空")
                    # print(filteredStrategys)

            if searchPeopleNumber and searchDays:
                    for one in strategys:
                        if one.get('peopleNumber') == int(searchPeopleNumber) and one.get('days') == int(searchDays):
                            # print("均符合")
                            if one not in filteredStrategys:
                                filteredStrategys.append(one);
                    # print(" 人数，天数都不空")
                    # print(filteredStrategys)

            if searchPeopleNumber and searchBudget:
                    for one in strategys:
                        if one.get('peopleNumber') == int(searchPeopleNumber) and one.get('budget') <= int(searchBudget):
                            # print("均符合")
                            if one not in filteredStrategys:
                                filteredStrategys.append(one);
                    # print(" 人数，预算都不空")
                    # print(filteredStrategys)

            if searchDays and searchBudget:
                    for one in strategys:
                        if one.get('days') == int(searchDays) and one.get('budget') <= int(searchBudget):
                            # print("均符合")
                            if one not in filteredStrategys:
                                filteredStrategys.append(one);
                    # print(" 天数,预算都不空")
                    # print(filteredStrategys)

            if searchPeopleNumber:
                    # print("searchPeopleNumber:"+searchPeopleNumber);
                    # if isinstance(searchPeopleNumber, int):
                    #     print("a is int")
                    # else:
                    #     print("a is not int")
                    for one in strategys:
                        # print(one.get('peopleNumber'));
                        if one.get('peopleNumber') == int(searchPeopleNumber):
                            print("符合")
                            if one not in filteredStrategys:
                                print(one)
                                filteredStrategys.append(one);
                    # print("筛选后的攻略")
                    # print(filteredStrategys)
                    # print(" 人数不空")
                    # print(filteredStrategys)

            if searchDays:
                    for one in strategys:
                        # print(one.get('searchDays'));
                        if one.get('days') == int(searchDays):
                            if one not in filteredStrategys:
                                print(one)
                                filteredStrategys.append(one);
                    # print(" 天数不空")
                    # print(filteredStrategys)

            if searchBudget:
                    for one in strategys:
                        # print(one.get('searchBudget'));
                        if one.get('budget') <= int(searchBudget):
                            if one not in filteredStrategys:
                                print(one)
                                filteredStrategys.append(one);
                    # print(" 预算不空")
                    # print(filteredStrategys)
            if not searchPeopleNumber and not searchDays and not searchBudget:
                filteredStrategys=strategys
            citys=request.session['citys']
            spots = request.session['spots']
            return render(request, "../templates/complete/strategyListPage.html", {'strategyList': filteredStrategys,
                                                                          'searchPeopleNumber': searchPeopleNumber,
                                                                          'searchDays': searchDays,
                                                                          'searchBudget':searchBudget,
                                                                          'searchKeywords':searchKeywords,
                                                                                   'citys':citys,
                                                                                   'spots':spots
                                                                          })
        else:
            # 搜索功能
            searchKeywords = request.POST.get('searchKeywords')
            cursor = connection.cursor();
            strategyList=[];

            if searchKeywords:
                # 找到了所有符合标准的攻略Id攻略
                strategyIds = searchStrategyIds(searchKeywords);
                for strategyId in strategyIds:
                    cursor.execute(
                        'select strategyTitle, budget, name, days, peopleNumber, content, diggNumber, createDate, strategyId,coverUrl from Frog_strategy, Frog_member where email=memberEmail_id and strategyId=\'{}\''.format(strategyId));
                    strategy = dictfetchall(cursor);
                    strategyList += strategy;
                print('符合标准的strategyList：');
                print(strategyList);
                # 保存搜索的攻略ID
                request.session['strategyIdsToFilter'] = strategyIds;
                request.session['searchKeywords']=searchKeywords;

                # 搜索符合标准的城市和景点
                citys = searchCity(request.session['searchKeywords'])
                spots = searchSpot(request.session['searchKeywords'])
                print(citys)
                print(spots)
                request.session['citys'] = citys;
                request.session['spots'] = spots;
            else:
                cursor.execute(
                    'select strategyTitle, budget, name, days, peopleNumber, content, diggNumber, createDate, strategyId,coverUrl from Frog_strategy, Frog_member where email=memberEmail_id');
                strategyList = dictfetchall(cursor);
                print(strategyList);
                request.session['strategyIdsToFilter']='';
                request.session['searchKeywords']='';
                # 搜索所有的城市和景点
                citys = searchCity(request.session['searchKeywords'])
                spots = searchSpot(request.session['searchKeywords'])
                print(citys)
                print(spots)
                request.session['citys'] = citys;
                request.session['spots'] = spots;

            return render(request, "../templates/complete/strategyListPage.html", {'strategyList': strategyList, 'searchKeywords':searchKeywords,'citys':citys,'spots':spots
                                                                          })
    if request.method=="GET":
        print("运行到这里了")
        cursor = connection.cursor();
        if request.session['searchKeywords']!='':
            searchKeywords=request.session['searchKeywords'];

            # 搜索符合标准的攻略
            strategyIds = searchStrategyIds(searchKeywords);
            strategyList=[];
            for strategyId in strategyIds:
                cursor.execute(
                    'select strategyTitle, budget, name, days, peopleNumber, content, diggNumber, createDate, strategyId,coverUrl from Frog_strategy, Frog_member where email=memberEmail_id and strategyId=\'{}\''.format(
                        strategyId));
                strategy = dictfetchall(cursor);
                strategyList += strategy;
            print('符合标准的strategyList：');
            print(strategyList);
            request.session['strategyIdsToFilter'] = strategyIds;

            # 搜索符合标准的城市和景点
            citys = searchCity(request.session['searchKeywords'])
            spots = searchSpot(request.session['searchKeywords'])
            print(citys)
            print(spots)
            request.session['citys'] = citys;
            request.session['spots'] = spots;
            return render(request, "../templates/complete/strategyListPage.html", {'strategyList': strategyList,'searchKeywords':searchKeywords,'citys':citys,'spots':spots})
        else:
            # 搜索所有的攻略
            cursor.execute(
                'select strategyTitle, budget, name, days, peopleNumber, content, diggNumber, createDate, strategyId,coverUrl from Frog_strategy, Frog_member where email=memberEmail_id');
            strategys = dictfetchall(cursor);
            print(strategys);
            request.session['strategyIdsToFilter'] = '';
            # 搜索所有的城市和景点
            citys=searchCity(request.session['searchKeywords'])
            spots = searchSpot(request.session['searchKeywords'])
            print(citys)
            print(spots)
            request.session['citys'] = citys;
            request.session['spots'] = spots;
            return render(request, "../templates/complete/strategyListPage.html", {'strategyList':strategys,'citys':citys,'spots':spots})

def dictfetchall(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    ]

def searchStrategyIds(searchKeywords):
    cursor = connection.cursor();
    # 搜索关键词：景点、城市、用户名称或攻略名
    strategyIds = [];
    # 景点
    cursor.execute(
        'select strategyId from Frog_strategy, Frog_spotincluded where strategyId_id=strategyId and spotName_id LIKE \'%{}%\''.format(
            searchKeywords));
    dictCursor = dictfetchall(cursor);
    if dictCursor:
        for one in dictCursor:
            if one.get('strategyId') not in strategyIds:
                strategyIds.append(one.get('strategyId'));
    # 城市
    cursor.execute(
        'select strategyId from Frog_strategy, Frog_cityincluded where strategyId_id=strategyId and cityName_id=\'{}\''.format(
            searchKeywords));
    dictCursor = dictfetchall(cursor);
    if dictCursor:
        for one in dictCursor:
            if one.get('strategyId') not in strategyIds:
                strategyIds.append(one.get('strategyId'));
    # 用户名
    cursor.execute(
        'select strategyId from Frog_strategy, Frog_member where memberEmail_id=email and name LIKE \'%{}%\''.format(
            searchKeywords));
    dictCursor = dictfetchall(cursor);
    print("用户名搜索");
    print(dictCursor);
    if dictCursor:
        for one in dictCursor:
            if one.get('strategyId') not in strategyIds:
                strategyIds.append(one.get('strategyId'));
    # 攻略标题
    cursor.execute(
        'select strategyId from Frog_strategy where strategyTitle LIKE \'%{}%\''.format(searchKeywords));
    dictCursor = dictfetchall(cursor);
    if dictCursor:
        for one in dictCursor:
            if one.get('strategyId') not in strategyIds:
                strategyIds.append(one.get('strategyId'));

    print('符合标准的strategyIds：');
    print(strategyIds);
    return strategyIds

def searchCity(searchKeywords):
    cursor = connection.cursor();
    if searchKeywords:
        cursor.execute(
            'select * from Frog_city where cityName LIKE \'%{}%\''.format(searchKeywords)
        )
    else:
        cursor.execute(
            'select * from Frog_city'
        )
    citys = dictfetchall(cursor)
    return citys

def searchSpot(searchKeywords):
    cursor = connection.cursor();
    if searchKeywords:
        cursor.execute(
            'select * from Frog_spot where spotName LIKE \'%{}%\''.format(searchKeywords)
        )
        spots = dictfetchall(cursor)
        cursor.execute(
            'select * from Frog_spot where cityName_id LIKE \'%{}%\''.format(searchKeywords)
        )
        cityTospots = dictfetchall(cursor)
        spots +=cityTospots
    else:
        cursor.execute(
            'select * from Frog_spot'
        )
        spots = dictfetchall(cursor)
    return spots

def enterUserPage(request):
    return render(request,"../templates/userPage.html")

def followList(request):
    email = request.user.username
    print("followList查看:" + email)
    if email:
        member = models.Member.objects.get(email=email)
        cursor = connection.cursor();
        cursor.execute(
            'select followingEmail_id from Frog_follow where followedEmail_id=\'{}\''.format(email)
        )
        fans=dictfetchall(cursor)
        cursor.execute(
            'select followedEmail_id from Frog_follow where followingEmail_id=\'{}\''.format(email)
        )
        concern=dictfetchall(cursor)
        return render(request, '../templates/complete/followListPage.html', {
                                                                           'member': member,
                                                                           'fans':fans,
                                                                           'concern':concern,
                                                                           })
    else:
        return render(request,"../templates/complete/followListPage.html")