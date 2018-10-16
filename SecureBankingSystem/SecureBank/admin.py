# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
<<<<<<< HEAD
from SecureBank.models import UserProfile

# Register your models here.
admin.site.register(UserProfile)
=======
from .models import *

# Register your models here.

admin.site.register(BankUser)
>>>>>>> master
