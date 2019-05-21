from django.db import models

# Create your models here.

class User(models.Model):
    '''用户表'''
    # email = models.ForeignKey(max_length=30,unique=True)
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=64)
    gender = models.IntegerField(max_length=32, default='男')
    telephone = models.IntegerField()


# 攻略表
class Strategy(models.Model):
    strategyId = models.AutoField(primary_key=True)
    peopleNumber = models.IntegerField(blank=True, null=True, default=0)
    budget = models.BigIntegerField(blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    strategyTitle = models.CharField(max_length=10, blank=True, null=True)


# 评论表
class Comment(models.Model):
    commentId = models.AutoField(primary_key=True)
    useremail = models.CharField(max_length=100, blank=True, null=True)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)


# 点赞表
class Digg(models.Model):
    useremail = models.CharField(max_length=100, blank=True, null=True)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)