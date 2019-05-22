from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# -------------------- wjh models begin --------------------
# 专家表
class Expert(models.Model):
    email = models.EmailField(primary_key=True)

    name = models.CharField(max_length=10)
    password = models.CharField(max_length=64)
    gender = models.CharField(max_length=10)
    telephone = models.CharField(max_length=11)

    introduction = models.TextField()
    seniority = models.IntegerField()
    tag = models.CharField(max_length=10)
    company = models.CharField(max_length=64)
    mark = models.FloatField()

# 会员表
class Member(models.Model):
    email = models.EmailField(primary_key=True)

    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    gender = models.CharField(max_length=64)
    telephone = models.CharField(max_length=64)

    location = models.CharField(max_length=64)
    followNum = models.IntegerField()
    fansNum = models.IntegerField()

# 订单表
class Order(models.Model):
    member = models.ForeignKey(db_column='member_email', to=Member, on_delete=models.CASCADE)
    expert = models.ForeignKey(db_column='expert_email', to=Expert, on_delete=models.CASCADE)
    state = models.IntegerField()
    date = models.DateTimeField(null=True)
    intent = models.TextField(null=True)
    comment = models.TextField(null=True)
    mark = models.FloatField(null=True)
# -------------------- wjh models end --------------------

# -------------------- xjy models begin --------------------
#用户表
# class User(models.Model):
#     email = models.EmailField(primary_key=True)
#     name = models.CharField(max_length=64)
#     password = models.CharField(max_length=64)
#     gender = models.CharField(max_length=64)
#     telephone = models.CharField(max_length=64)


class User(AbstractUser):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    gender = models.CharField(max_length=64)
    telephone = models.CharField(max_length=64)

    class Meta:
        db_table='user'

# -------------------- xjy models end --------------------

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
    # useremail = models.CharField(max_length=100, blank=True, null=True)
    useremail = models.ForeignKey('Member', on_delete=models.CASCADE,blank=True, null=True)
    strategy = models.ForeignKey('Strategy', on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)


# 点赞表
class Digg(models.Model):
    # useremail = models.CharField(max_length=100, blank=True, null=True)
    useremail=models.ForeignKey(Member,on_delete=models.CASCADE, blank=True, null=True)
    strategy=models.ForeignKey(Strategy,on_delete=models.CASCADE)
    # strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)


# -------------------- ylz models begin --------------------
# 餐厅表
class Restaurant(models.Model):
    restaurantName=models.CharField(max_length=30,primary_key=True)
    cityName=models.ForeignKey('City',on_delete=models.SET_NULL,null=True)
    location=models.CharField(max_length=60)
    telephone=models.CharField(max_length=20)
    pictureURL=models.TextField(max_length=200)
    speciality=models.CharField(max_length=30)
    averageConsume=models.PositiveIntegerField()

# 景点表
class Spot(models.Model):
    spotName=models.CharField(max_length=30,primary_key=True)
    cityName=models.ForeignKey('City', on_delete=models.SET_NULL,null=True)
    introduction=models.TextField(max_length=100)
    ticketPrice=models.PositiveIntegerField()
    location = models.CharField(max_length=60)
    spotTelephone=models.CharField(max_length=20)

# 城市表
class City(models.Model):
    cityName=models.CharField(max_length=10,primary_key=True)
    introduction = models.TextField(max_length=100)
    pictureURL=models.TextField(max_length=200)
    province=models.CharField(max_length=10)

# 餐厅攻略表
class RestaurantIncluded(models.Model):
    strategyId=models.ForeignKey('Strategy',on_delete=models.CASCADE)
    restaurantName=models.ForeignKey('Restaurant',on_delete=models.CASCADE)

# 景点攻略表
class SpotIncluded(models.Model):
    strategyId = models.ForeignKey('Strategy', on_delete=models.CASCADE)
    spotName = models.ForeignKey('Spot', on_delete=models.CASCADE)

# 城市攻略表
class CityIncluded(models.Model):
    strategyId = models.ForeignKey('Strategy', on_delete=models.CASCADE)
    cityName = models.ForeignKey('City', on_delete=models.CASCADE)


# 关注表
class Follow(models.Model):
    followedEmail=models.ForeignKey('Member',related_name='followed', on_delete=models.CASCADE)
    followingEmail=models.ForeignKey('Member',related_name='folllowing', on_delete=models.CASCADE)

# -------------------- ylz models end --------------------