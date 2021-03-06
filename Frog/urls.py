from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexpage, name='indexpage'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('update/', views.update, name='update'),
    path('personal/', views.personal, name='personal'),#查看历史攻略

    path('logout/', views.logoff, name='logout'),
    path('index/', views.indexpage, name='indexpage'),
    path('log/', views.log, name='log'),
    #  path('user/<userId>', views.user, name='user'), 用这个可以穿参数
    path('user/', views.user, name='user'),
    path('api/code/', views.code, name='code'),
    path('strategyList/',views.strategyList,name='strategyList'),
    path('strategyDetail/',views.enterUserPage,name='strategyDetail'),
    path('followList/',views.followList,name='followList'),

]