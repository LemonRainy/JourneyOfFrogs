from django.shortcuts import render


def expertOrderList(request):
    return render(request, '../templates/expertOrderListPage.html')


def expert(request):
    return render(request, '../templates/expertPage.html')

def orderHandling(request):
    return render(request, '../templates/orderHandlingPage.html')
