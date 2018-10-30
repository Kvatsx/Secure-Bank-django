# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User

from .models import *


admin.site.disable_action('delete_selected')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('Amount', 'Status','CreationTime', 'FromAccount', 'ToAccount')
    list_filter = ('Status','CreationTime', 'FromAccount', 'ToAccount')
    fields = ['Status']
    actions = ['approve', 'reject']

    def approve(self, request, queryset):
        if not request.user.get_profile().type_of_user == 'S':
            queryset = queryset.filter(Amount__lte = BankUser.MAX_REGULAR_EMPLOYEE)
        rows_updated = 0
        for obj in queryset:
            if obj.Status=='A':
                try:
                    obj.approve_transaction()
                    rows_updated+=1
                except:
                    print("error occured for transaction ", obj)
                    # mark the transaction as error
        if rows_updated == 1:
            message_bit = "1 Transaction was"
        else:
            message_bit = "%s Transactions were" % rows_updated
        self.message_user(request, "%s Approved" % message_bit)
    approve.short_description = "Approve selected transactions"

    def reject(self, request, queryset):
        if not request.user.type_of_user == 'S':
            queryset = queryset.filter(Amount__lte = BankUser.MAX_REGULAR_EMPLOYEE)  
        rows_updated = 0
        for obj in queryset:
            if obj.Status=='R':
                try:
                    obj.reject_transaction()
                    rows_updated+=1
                except:
                    print("error occured for transaction ", obj)
                    # mark the transaction as error
        if rows_updated == 1:
            message_bit = "1 Transaction was"
        else:
            message_bit = "%s Transactions were" % rows_updated
        self.message_user(request, "%s Rejected" % message_bit)
    reject.short_description = "Reject selected transactions"




class BankUserInline(admin.StackedInline):
    model = BankUser
    can_delete = False
    verbose_name_plural = 'bankuser'

class UserAdmin(BaseUserAdmin):
    inlines = (BankUserInline, )
    list_display = ('username', 'first_name', 'last_name', 'email', 'get_phone', 'get_address', 'get_type', 'is_staff')
    # fields = ['username', 'first_name', 'last_name', 'email', 'get_phone', 'get_address', 'get_type', 'is_staff']
    list_select_related = ('bankuser', )

    def get_phone(self, instance):
        return instance.bankuser.phone
    get_phone.short_description = 'Phone No.'

    def get_address(self, instance):
        return instance.bankuser.address
    get_address.short_description = 'Address'

    def get_type(self, instance):
        return instance.bankuser.type_of_user
    get_type.short_description = 'User Type'

    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return list()
    #     return super(UserAdmin, self).get_inline_instances(request, obj)


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


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.register(BankUser)