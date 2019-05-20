from django.shortcuts import render


def expertOrderList(request):
    return render(request, '../templates/expertOrderListPage.html')
