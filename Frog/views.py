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
        reciever = request.GET['email']
        # 发送邮件
        print(reciever, msg)
        send_mail(title, str(msg), email_from, [reciever])

        return HttpResponse("邮件已发送！")

#查看历史攻略
def personal(request):
    email = request.session.get('email')
    if email:
        strategies = models.Strategy.objects.filter(memberEmail=email)
        return render(request, '../templates/personalPage.html', {'strategies': strategies})
    else:
        return redirect('/personal')

def filterStrategy(request):
    if request.method== "POST":
        if request.POST.get('filterOrSearch'):
            print(request.POST)
            searchSpot = request.POST.get('searchSpot')
            searchPeopleNumber = request.POST.get('searchPeopleNumber')
            searchDays = request.POST.get('searchDays')
            searchBudget = request.POST.get('searchBudget')
            # searchSortord = request.POST.get('searchSortord')

            strategys = models.Strategy.objects.filter(peopleNumber=searchPeopleNumber,days=searchDays,budget=searchBudget)
            print(strategys)
            return render(request, "../templates/strategyListPage.html", {'strategyList': strategys,
                                                                          })
        else:
            # 搜索功能
            searchCity = request.POST.get('searchCity')
            cursor = connection.cursor();
            cursor.execute('select * from Frog_city, Frog_strategy, Frog_cityincluded where cityName=cityName_id and strategyId=strategyId_id');
            dictCursor = dictfetchall(cursor);
            strategyList=[];
            if searchCity:
                for strategy in dictCursor:
                    if(strategy.get('cityName')==searchCity):
                        strategyList.append(strategy);
            else:
                strategyList = dictCursor;

            return render(request, "../templates/strategyListPage.html", {'strategyList': strategyList
                                                                          })
    if request.method=="GET":
        cursor = connection.cursor();
        cursor.execute(
            'select * from Frog_city, Frog_strategy, Frog_cityincluded where cityName=cityName_id and strategyId=strategyId_id');
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