from django.urls import path
from . import views_wjh

urlpatterns = [
    path('expertOrderList', views_wjh.expertOrderList, name='expertOrderList'),
    path('expert', views_wjh.expert, name='expert'),
    path('orderHandling', views_wjh.orderHandling, name='orderHandling'),
    path('changeInfo', views_wjh.changeInfo, name='changeInfo'),
    path('changePassword', views_wjh.changePassword, name='changePassword'),
    path('acceptOrder', views_wjh.acceptOrder, name='acceptOrder'),
    path('refuseOrder', views_wjh.refuseOrder, name='refuseOrder'),
]