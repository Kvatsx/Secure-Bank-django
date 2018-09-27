# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE




class BankUser(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=CASCADE, primary_key=True)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username



