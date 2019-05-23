from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('modifyPassword/', views.modifyPassword, name='modifyPassword'),
    path('historyOrder/', views.historyOrder, name='historyOrder'),

    path('logout/', views.logoff, name='logout'),
    path('index/', views.indexpage, name='indexpage'),
    path('log/', views.log, name='log'),
    #  path('user/<userId>', views.user, name='user'), 用这个可以穿参数
    path('customize/', views.customize, name='customize'),
    path('user/', views.user, name='user'),
]