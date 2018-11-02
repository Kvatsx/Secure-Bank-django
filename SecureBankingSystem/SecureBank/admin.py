# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import *

from Crypto.PublicKey import RSA

# admin.site.disable_action('delete_selected')

# class TransactionForm(UserChangeForm):
#     def __init__(self, *args, **kwargs):
#         super(BankUserForm, self).__init__(*args, **kwargs)
#         self.fields['first_name'].required = True
#         self.fields['email'].required = True

# create the public and private key
def pki_util(obj):
    print("hello new user")
    key = RSA.generate(2048,e=1131)
    binPrivKey = key.exportKey('PEM')
    binPubKey =  key.publickey().exportKey('PEM')
    p1=binPubKey.decode('ascii')
    p2=binPrivKey.decode('ascii')
    obj.bankuser.publicKey=p1.replace('\n','n')
    obj.bankuser.save()
    print("assigned", obj.bankuser.publicKey)
    # obj.privateKey=p2.replace('\n','n')


@admin.register(ProfileEditRequest)
class ProfileEditRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'newEmail', 'Status')
    list_filter = ('Status', 'user',)
    # fields = ('user', 'Status', 'newEmail')
    actions = ['approve', 'reject']


    def get_newEmail(self, instance):
        return instance.email
    get_newEmail.short_description = 'New Email'

    def get_username(self, instance):
        return instance.username
    get_username.short_description = 'username'
        
    def change_view(self,request,object_id,extra_content=None):
        self.exclude = ('user', 'Status', 'newEmail')
        return super(ProfileEditRequestAdmin, self).change_view(request,object_id)

    def add_view(self,request,extra_content=None):
        self.exclude = ()
        return super(ProfileEditRequestAdmin, self).add_view(request)
        
    def approve(self, request, queryset):
        selected = len(queryset)
        rows_updated = 0
        rows_problem = 0
        different_status = 0
        for obj in queryset:
            if obj.Status=='A':
                try:
                    obj.ApproveProfileEditRequest()
                    rows_updated+=1
                except:
                    rows_problem+=1
                    obj.mark_error()
                    print("error occured while updating ", obj)
                    # mark the transaction as error
            else:
                different_status+=1
        if rows_updated == 1:
            message_bit = "1 Edit Request was"
        else:
            message_bit = "%s Edit Requests were" % rows_updated
        msg = "{} Approved".format(message_bit)
        if rows_problem > 0:
            msg = msg + "{} could not Approve".format(rows_problem)
        if different_status > 0:
            msg = msg + ". {} don't have status 'Approval Required'".format(different_status)
        self.message_user(request, msg)
    approve.short_description = "Approve selected Edit Requests"

    def reject(self, request, queryset):
        selected = len(queryset)
        rows_updated = 0
        rows_problem = 0
        different_status = 0
        for obj in queryset:
            if obj.Status=='A':
                try:
                    obj.RejectProfileEditRequest()
                    rows_updated+=1
                except:
                    rows_problem+=1
                    obj.mark_error()
                    print("error occured while rejecting ", obj)
                    # mark the transaction as error
            else:
                different_status+=1
        if rows_updated == 1:
            message_bit = "1 Edit Request was"
        else:
            message_bit = "%s Edit Requests were" % rows_updated
        msg = "{} Rejected".format(message_bit)
        if rows_problem > 0:
            msg = msg + "{} could not Reject".format(rows_problem)
        if different_status > 0:
            msg = msg + ". {} don't have status 'Approval Required'".format(different_status)
        self.message_user(request, msg)
    reject.short_description = "Reject selected Edit Requests"

    

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('Amount','Type', 'Status', 'FromAccount', 'ToAccount', 'CreationTime')
    list_filter = ('Status', 'Type', 'CreationTime', 'FromAccount', 'ToAccount')
    # fields = ('Amount', 'FromAccount', 'ToAccount', 'Employee')

    def add_view(self,request,extra_content=None):
        self.exclude = ()
    #     # self.fields['Amount'].required = True
    #     # self.fields['Type'].required = True
    #     # self.fields['Status'].required = True
    #     # self.fields['FromAccount'].required = True
    #     # self.fields['ToAccount'].required = True
    #     # self.fields['CreationTime'].required = True
    #     # self.fields['Employee'].required = True
        return super(TransactionAdmin, self).add_view(request)

    def change_view(self,request,object_id,extra_content=None):
        self.exclude = ('Amount', 'Status', 'CreationTime', 'FromAccount', 'ToAccount', 'Employee', 'Type')
        return super(TransactionAdmin, self).change_view(request,object_id)
    
    # def formfield_for_choice_field(self, db_field, request, **kwargs):
    #     if db_field.name == "Status":
    #         kwargs['choices'] = (
    #             ('A', 'Approval required'),
    #         )

    #     if db_field.name == "Type":
    #         kwargs['choices'] = (
    #             ('T', 'Transfer'),
    #         )
    #     return super(TransactionAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        obj.Status = 'A'
        obj.Type = 'T'
        super().save_model(request, obj, form, change)
   
    actions = ['approve', 'reject']

    def approve(self, request, queryset):
        selected = len(queryset)
        if not request.user.bankuser.type_of_user == 'S':
            queryset = queryset.filter(Amount__lte = BankUser.MAX_REGULAR_EMPLOYEE)
        rows_filtered = len(queryset)
        rows_updated = 0
        rows_problem = 0
        different_status = 0
        for obj in queryset:
            if obj.Status=='A':
                try:
                    obj.approve_transaction()
                    rows_updated+=1
                except:
                    rows_problem+=1
                    obj.mark_error()
                    print("error occured for transaction ", obj)
                    # mark the transaction as error
            else:
                different_status+=1
        if rows_updated == 1:
            message_bit = "1 Transaction was"
        else:
            message_bit = "%s Transactions were" % rows_updated
        msg = "{} Approved".format(message_bit)
        if rows_problem > 0:
            msg = msg + "{} could not Approve".format(rows_problem)
        if different_status > 0:
            msg = msg + ". {} don't have status 'Approval Required'".format(different_status)
        if selected-rows_filtered > 0:
            msg = msg + ". {} Ignored. Permission Required for Amount greater than {}".format(selected-rows_filtered, BankUser.MAX_REGULAR_EMPLOYEE)
        self.message_user(request, msg)
    approve.short_description = "Approve selected transactions"
    
    def reject(self, request, queryset):
        selected = len(queryset)
        if not request.user.bankuser.type_of_user == 'S':
            queryset = queryset.filter(Amount__lte = BankUser.MAX_REGULAR_EMPLOYEE)  
        rows_filtered = len(queryset)
        rows_updated = 0
        rows_problem = 0
        different_status = 0
        for obj in queryset:
            if obj.Status=='A':
                try:
                    obj.reject_transaction()
                    rows_updated+=1
                except:
                    rows_problem+=1
                    obj.mark_error()
                    print("error occured for transaction ", obj)
                    # mark the transaction as error
            else:
                different_status+=1
        if rows_updated == 1:
            message_bit = "1 Transaction was"
        else:
            message_bit = "%s Transactions were" % rows_updated
        msg = "{} Rejected.".format(message_bit)
        if rows_problem > 0:
            msg = msg + " {} could not Reject.".format(rows_problem)
        if different_status > 0:
            msg = msg + ". {} don't have status 'Approval Required'".format(different_status)
        if selected-rows_filtered > 0:
            msg = msg + " {} Ignored. Permission Required for Amount greater than {}".format(selected-rows_filtered, BankUser.MAX_REGULAR_EMPLOYEE)
        self.message_user(request, msg)
    reject.short_description = "Reject selected transactions"

class BankUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(BankUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True


class BankUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(BankUserChangeForm, self).__init__(*args, **kwargs)
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
    form = BankUserChangeForm
    add_form = BankUserForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )

    inlines = (BankUserInline, )
    list_display = ('username', 'first_name', 'last_name', 'email', 'get_phone', 'get_address', 'get_type','is_staff', 'get_publicKey')
    # fields = ['username', 'first_name', 'last_name', 'email', 'get_phone', 'get_address', 'get_type', 'is_staff']
    list_select_related = ('bankuser', )

    def get_publicKey(self, instance):
        return instance.bankuser.publicKey
    get_publicKey.short_description = 'Public Key'

    def get_phone(self, instance):
        return instance.bankuser.phone
    get_phone.short_description = 'Phone No.'

    def get_address(self, instance):
        return instance.bankuser.address
    get_address.short_description = 'Address'

    def get_type(self, instance):
        return instance.bankuser.type_of_user
    get_type.short_description = 'User Type'

    def response_add(self, request, new_object):
        pki_util(new_object)
        return super(UserAdmin, self).response_add(request, new_object)

    # def save_model(self, request, obj, form, change):
    #     print("change", change)
    #     super().save_model(request, obj, form, change)
    #     print("got", obj.bankuser.publicKey, obj)


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