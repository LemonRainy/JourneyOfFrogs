from django.urls import path
from . import views_zxd

urlpatterns = [
    path('share/', views_zxd.share, name='share'),
    path(r'getimage/', views_zxd.getimage, name='getimage'),
]