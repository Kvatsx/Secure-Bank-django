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
from django.db.models import CASCADE
from pyotp import random_base32, TOTP, totp



class BankUser(models.Model):

    class Meta:
        permissions = (
            ("is_External_User", "User has customer permission"),
            ("is_Internal_User", "Employee has permissions to access User data"),
            ("super_user", "For inspection purpose"),
        )
    # UID ( Primary Key ), Last Login, Last transaction, last password change, failed login attempt, type of user
    user = models.OneToOneField(User, unique=True, on_delete=CASCADE, primary_key=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=250)
    otp_value = models.CharField(max_length=16, default='0', editable=False)
    # ListCharField (Internal User, Account access for Internal user). https://django-mysql.readthedocs.io/en/latest/model_fields/list_fields.html

    # TODO: Need to add OTP creation time (for validity of OTP)

    def __str__(self):
        return self.user.username

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

# class Account(models.Model)
#     TODO: Need to create Account SQLite Table here
#   account number, user object
#
# class Transaction(models.Model):
#     TODO: Need to create Transaction SQLite Table here
    # to, from , timestamp(object), amount, status(pending, accepted, rejected), UID,
