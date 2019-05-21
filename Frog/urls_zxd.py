from django.urls import path
from . import views_zxd

urlpatterns = [
    path('share/', views_zxd.share, name='share'),
    path(r'article/<strategyId>', views_zxd.detailArticle, name='detailArticle'),
    path(r'getimage/', views_zxd.getimage, name='getimage'),
    path(r'api/digg/', views_zxd.digg, name='digg'),
]