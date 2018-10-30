# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import *


# admin.site.disable_action('delete_selected')

# class TransactionForm(UserChangeForm):
#     def __init__(self, *args, **kwargs):
#         super(BankUserForm, self).__init__(*args, **kwargs)
#         self.fields['first_name'].required = True
#         self.fields['email'].required = True


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('Amount', 'Status','CreationTime', 'FromAccount', 'ToAccount')
    list_filter = ('Status','CreationTime', 'FromAccount', 'ToAccount')
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ()}
        ),
    )
    actions = ['approve', 'reject']

    def approve(self, request, queryset):
        selected = len(queryset)
        if not request.user.bankuser.type_of_user == 'S':
            queryset = queryset.filter(Amount__lte = BankUser.MAX_REGULAR_EMPLOYEE)
        rows_filtered = len(queryset)
        rows_updated = 0
        rows_problem = 0
        for obj in queryset:
            if obj.Status=='A':
                try:
                    obj.approve_transaction()
                    rows_updated+=1
                except:
                    rows_problem+=1
                    print("error occured for transaction ", obj)
                    # mark the transaction as error
        if rows_updated == 1:
            message_bit = "1 Transaction was"
        else:
            message_bit = "%s Transactions were" % rows_updated
        msg = "{} Approved".format(message_bit)
        if rows_problem > 0:
            msg = msg + "{} could not Approve".format(rows_problem)
        if selected-rows_filtered > 0:
            msg = msg + " {} Ignored. Permission Required for Amount greater than {}".format(selected-rows_filtered, BankUser.MAX_REGULAR_EMPLOYEE)
        self.message_user(request, msg)
    approve.short_description = "Approve selected transactions"
    
    def reject(self, request, queryset):
        selected = len(queryset)
        if not request.user.bankuser.type_of_user == 'S':
            queryset = queryset.filter(Amount__lte = BankUser.MAX_REGULAR_EMPLOYEE)  
        rows_filtered = len(queryset)
        rows_updated = 0
        rows_problem = 0
        for obj in queryset:
            if obj.Status=='R':
                try:
                    obj.reject_transaction()
                    rows_updated+=1
                except:
                    rows_problem+=1
                    print("error occured for transaction ", obj)
                    # mark the transaction as error
        if rows_updated == 1:
            message_bit = "1 Transaction was"
        else:
            message_bit = "%s Transactions were" % rows_updated
        msg = "{} Rejected.".format(message_bit)
        if rows_problem > 0:
            msg = msg + " {} could not Reject.".format(rows_problem)
        if selected-rows_filtered > 0:
            msg = msg + " {} Ignored. Permission Required for Amount greater than {}".format(selected-rows_filtered, BankUser.MAX_REGULAR_EMPLOYEE)
        self.message_user(request, msg)
    reject.short_description = "Reject selected transactions"

class BankUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(BankUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True


class BankUserInlineFormset(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BankUserInlineFormset, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False

class BankUserInline(admin.StackedInline):
    model = BankUser
    fields = ['phone', 'type_of_user']
    formset = BankUserInlineFormset
    can_delete = False
    verbose_name_plural = 'bankuser'

class UserAdmin(BaseUserAdmin):
    form = BankUserForm
    add_form = BankUserForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )

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