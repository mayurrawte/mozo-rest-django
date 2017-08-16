from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class UserDetails(models.Model):
    userId = models.ForeignKey('auth.User', related_name='userDetail', on_delete=models.CASCADE)
    userFacebookId = models.CharField(max_length=100)
    userGoogleId = models.CharField(max_length=100)
    userPicUrl = models.URLField()
    friends = models.TextField()


class Account(models.Model):
    accountUser = models.ForeignKey('auth.User', related_name="Account", on_delete=models.CASCADE)
    accountAmount = models.FloatField()


class Transactions(models.Model):
    toUser = models.ForeignKey('auth.User', related_name="transactionTo", on_delete=models.CASCADE)
    fromUser = models.ForeignKey('auth.User', related_name="transactionFrom", on_delete=models.CASCADE)
    transactionType = models.CharField(choices=(('refund','Refundable Transaction'),('nonrefund','Non Refundable Transaction')), max_length=20, default='nonrefund')
    transactionAmount = models.FloatField()
    transactionStatus = models.BooleanField()


class Expenses(models.Model):
    expenseUser = models.ForeignKey('auth.User', related_name="Expenses", on_delete=models.CASCADE)
    expenseType = models.CharField(choices=(('food', 'food'), ('education', 'education'), ('travel', 'travel'), ('shopping', 'shopping'), ('extra', 'extra'), ('living', 'living')), default='extra', max_length=20)
    expenseItem = models.CharField(max_length=100)
    expenseAmount = models.FloatField()
    expenseTime = models.DateTimeField(auto_created=True, auto_now=True)
