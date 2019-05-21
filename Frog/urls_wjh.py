from django.urls import path
from . import views_wjh

urlpatterns = [
    path('expertOrderList', views_wjh.expertOrderList, name='expertOrderList'),
    path('expert', views_wjh.expert, name='expert'),
    path('orderHandling', views_wjh.orderHandling, name='orderHandling'),
]