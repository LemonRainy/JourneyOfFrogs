from django.urls import path
from . import views_wjh

urlpatterns = [
    path('expertOrderList', views_wjh.expertOrderList, name='expertOrderList'),
]