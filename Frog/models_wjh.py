# Create your models here.
from django.db import models


class Expert(models.Model):
    email = models.EmailField()

    name = models.CharField(max_length=10)
    password = models.CharField(max_length=64)
    gender = models.CharField(max_length=10)
    telephone = models.CharField(max_length=11)

    introduction = models.TextField()
    seniority = models.IntegerField()
    tag = models.CharField(max_length=10)
    company = models.CharField(max_length=64)
    mark = models.FloatField()


class Order(models.Model):
    memberEmail = models.EmailField()
    expertEmail = models.EmailField()
    state = models.IntegerField()
    comment = models.TextField()
    mark = models.FloatField()


class Member(models.Model):
    email = models.EmailField()

    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    gender = models.CharField(max_length=64)
    telephone = models.CharField(max_length=64)

    location = models.CharField(max_length=64)
    followNum = models.IntegerField()
    fansNum = models.IntegerField()