from django.db import models

# Create your models here.

class User(models.Model):
    '''用户表'''
    genders = (
        (0, '男'),
        (1, '女'),
    )

    email = models.ForeignKey(max_length=30,unique=True)
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=64)
    gender = models.IntegerField(max_length=32, choices=genders, default='男')
    telephone = models.IntegerField()


