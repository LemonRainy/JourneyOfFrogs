# Create your models here.
from django.db import models

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


class Member(models.Model):
    email = models.EmailField(primary_key=True)

    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    gender = models.CharField(max_length=64)
    telephone = models.CharField(max_length=64)

    location = models.CharField(max_length=64)
    followNum = models.IntegerField()
    fansNum = models.IntegerField()


class Order(models.Model):
    member = models.ForeignKey(db_column='member_email', to=Member, on_delete=models.CASCADE)
    expert = models.ForeignKey(db_column='expert_email', to=Expert, on_delete=models.CASCADE)
    state = models.IntegerField()
    date = models.DateTimeField(null=True)
    intent = models.TextField(max_length=300, null=True)
    comment = models.TextField(null=True)
    mark = models.FloatField(null=True)
    travelNum = models.CharField(max_length=30, null=True)
    childNum = models.CharField(max_length=30, null=True)
    departureCity = models.CharField(max_length=30, null=True)
    destinationCity = models.CharField(max_length=30, null=True)
    departureTime = models.DateTimeField(null=True)
    destinationTime = models.DateTimeField(null=True)
