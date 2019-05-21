from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout

# Create your views here.


def index(request):
    return render(request, '../templates/index.html')

def login(request):
    if request.method == 'POST':
        user = authenticate(request,username=request.POST['email'],password=request.POST['password'])
        if user is None:
            return render(request,'../templates/loginPage.html',{'Error','用户名不存在!'})
        else:
            login(request,user)
            redirect('myauth:index')

def register(request):
    pass

def modifyPassword(request):
    pass

def viewHistory(request):
    pass
