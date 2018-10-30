# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('Amount', 'Status','CreationTime', 'FromAccount', 'ToAccount')
    list_filter = ('Status','CreationTime', 'FromAccount', 'ToAccount')
    fields = ['Status']


# class ProfileInline(admin.StackedInline):
#     model = BankUser
#     can_delete = False
#     verbose_name_plural = 'Profile'
#     fk_name = 'user'

# class CustomUserAdmin(UserAdmin):
#     inlines = (ProfileInline, )

#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# class BankUserAdmin(UserAdmin):
#     model = BankUser
#     list_display = ('user', 'user.first_name', 'type_of_user', 'phone','EmailID', 'address')
#     list_filter = ('user', 'type_of_user', 'phone','EmailID', 'address')
#     fields = ('user', 'type_of_user', 'phone','EmailID')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('AccountNumber', 'AccountHolder','Balance')
    list_filter = ('AccountNumber', 'AccountHolder','Balance')
    fields = ('AccountNumber', 'AccountHolder','Balance')


# admin.site.unregister(User)
# admin.site.register(BankUser, UserAdmin)
admin.site.register(BankUser)