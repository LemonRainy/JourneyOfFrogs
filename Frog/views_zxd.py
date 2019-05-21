from django.shortcuts import render, redirect, HttpResponse
import time
from django.conf import settings
# Create your views here.


def share(request):
    if request.method == "GET":
        return render(request, '../templates/complete/shareStrategyPage.html')
    if request.method == "POST":
        content = request.POST.get('content')
        print(content)
        return render(request, '../templates/complete/shareStrategyPage.html')


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


