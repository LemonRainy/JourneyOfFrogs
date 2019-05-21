from django.shortcuts import render, redirect, HttpResponse
import time
from django.conf import settings
from . import models
# Create your views here.


# 分享攻略
def share(request):
    if request.method == "GET":
        return render(request, '../templates/complete/shareStrategyPage.html')
    if request.method == "POST":
        content = request.POST.get('content')
        title = request.POST.get('title')
        newstrategy = models.Strategy.objects.create(peopleNumber=0, budget=0, content=content,
                                                     strategyTitle=title)
        return redirect('/article/' + str(newstrategy.strategyId))
        # print(request.POST)
        # return render(request, '../templates/complete/shareStrategyPage.html')


def detailArticle(request, strategyId):
    print(strategyId)
    useremail = 1 # 假定用户邮箱
    digg_tag = 0  # 初始点赞状态
    if request.method == "GET":
        if not models.Strategy.objects.filter(strategyId=strategyId):
            error = "strategy not found"
            return render(request, '../templates/complete/article.html', {'error': error})

    strategy = models.Strategy.objects.get(strategyId=strategyId)
    if request.method == "POST":
        commentcontent = request.POST.get("commentContent")
        print(commentcontent)
        models.Comment.objects.create(useremail=1, content=commentcontent, strategy=strategy)

    if models.Digg.objects.filter(useremail=useremail, strategy=strategy):
        digg_tag = 1

    comments = models.Comment.objects.filter(strategy=strategy)
    return render(request, '../templates/complete/strategyDetailPage.html', {'strategy': strategy, 'comments': comments, 'digg_tag': digg_tag})



# 图片上传接口
def getimage(request):
    pic = request.FILES.get('file')
    uid = request.POST.get('uid')
    ct = time.time()
    date_head = 'IMG_' + str(time.strftime("%Y%m%d_%H%M%S", time.localtime()))
    date_secs = (ct - int(ct)) * 1000
    filename = "%s_%03d" % (date_head, date_secs) + '.jpg'
    save_path = '%s%s' % (settings.IMG_ROOT, filename)  # pic.name 上传文件的源文件名
    print(save_path)
    with open(save_path, 'wb') as f:
        # 3.获取上传文件的内容并写到创建的文件中
        for content in pic.chunks():  # pic.chunks() 上传文件的内容。
            f.write(content)
    return HttpResponse(str(filename))


# 点赞接口
def digg(request):
    # 差把保存点赞
    useremail = 1
    if request.method == "GET":
        strategy = models.Strategy.objects.get(strategyId=request.GET.get('strategyId'))
        if models.Digg.objects.filter(useremail=useremail, strategy=strategy):
            models.Digg.objects.get(useremail=useremail, strategy=strategy).delete()
            return HttpResponse(0)
        else:
            models.Digg.objects.create(useremail=useremail, strategy=strategy)
            return HttpResponse(1)
    else:
        return HttpResponse(-1)
