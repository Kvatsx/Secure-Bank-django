# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     number = models.IntegerField(default=0)


# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = UserProfile.objects.create(user=kwargs['instance'])
#
#
# post_save.connect(create_profile, sender=User)

from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE, SET_NULL
from pyotp import random_base32, TOTP, totp



class BankUser(models.Model):
    class Meta:
        permissions = (
            ("is_External_User", "Customer of bank"),
            ("is_Internal_User", "Employee has permissions to access User data"),
        )

    TYPES = (
        ('R', 'Regular Employee'),
        ('S', 'System Manager'),
        ('A', 'Admin'),
        ('I', "Individual Customer"),
        ('O', 'Organization'),
    )
    # UID ( Primary Key ), Last Login, Last transaction, last password change, failed login attempt, type of user
    user = models.OneToOneField(User, unique=True, on_delete=CASCADE, primary_key=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=250)
    otp_value = models.CharField(max_length=16, default='0', editable=False)
    type_of_user = models.CharField(max_length=1, choices=TYPES)
    # ListCharField (Internal User, Account access for Internal user). https://django-mysql.readthedocs.io/en/latest/model_fields/list_fields.html

    # TODO: Need to add OTP creation time (for validity of OTP)

    def __str__(self):
        return self.user.username +" "+ self.type_of_user

    # https://pyotp.readthedocs.io/en/latest/
    def generateOTP(self):
        self.otp_value = random_base32()
        self.save()
        return totp.TOTP(self.otp_value).provisioning_uri(self.user.username, issuer_name="Secure Banking System")

    def verifyOTP(self, otp):
        pot = TOTP(self.otp_value)
        return pot.verify(otp)

# class Payment(models.Model):
#     # TODO: Need to create Payment SQLite Table here
#     organization = models.ForeignKey(BankUser, related_name="merchant", null=True)
#     user = models.ForeignKey(Account, related_name='user', null=True)
#     transaction = models.ForeignKey(Transaction, related_name='transaction')
    #

class Account(models.Model):

    AccountNumber = models.IntegerField(primary_key=True, unique=True)
    AccountHolder = models.ForeignKey(BankUser, null=True, on_delete=True)
    Balance = models.IntegerField(default=0, editable=True)

    def __str__(self):
        return self.AccountHolder.user.username + " " + str(self.AccountNumber) + " " + str(self.Balance)


class Transaction(models.Model):
    DEBIT = 0
    CREDIT = 1
    STATUS = (
        ('O', 'OTP'),
        ('A', 'Internal User Approval required'),
        ('P', 'Complete'),
        ('R', 'Rejected by Internal User'),
        ('E', 'Error occured during transaction'),
    )
    Employee = models.ForeignKey(BankUser, null=True, blank=True, on_delete=SET_NULL)
    FromAccount = models.ForeignKey(Account, null=True, related_name='FromAccount', on_delete=SET_NULL, blank=True)
    ToAccount = models.ForeignKey(Account, null=True, related_name='ToAccount', on_delete=SET_NULL, blank=True)
    Amount = models.IntegerField(default=0, editable=False)
    Status = models.CharField(max_length=1, choices=STATUS, editable=False)

    # to, from , timestamp(object), amount, status(pending, accepted, rejected), UID,

    def __str__(self):
        return str(self.id) + " " + str(self.FromAccount.AccountNumber) + " " + str(self.ToAccount.AccountNumber) + " " + str(self.Amount)

