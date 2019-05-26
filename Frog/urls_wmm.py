from django.urls import path
from . import views_wmm

urlpatterns = [
    path('customize/', views_wmm.customize, name='customize'),
    path('orderList/', views_wmm.orderList, name='orderList'),
    path('orderDetail/<orderID>', views_wmm.orderDetail, name='orderDetail'),
    # path('orderDetail/', views_wmm.saveComment, name='saveComment'),
]