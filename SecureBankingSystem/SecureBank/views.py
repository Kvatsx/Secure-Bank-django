# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib
import json
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.urls import reverse

from .utils import get_value, SecureBankException
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from .models import Transaction
from .decorators import external_user_required, internal_user_required

# Create your views here.

def index(request):
    return redirect('login')

def login_user(request):
    if request.user.is_authenticated:
        if (request.user.is_staff):
            return redirect('/admin/')  # change "user" accordingly for internal user
        else:
            return redirect('user')
    args = {
        'wrong_credentials' : False
    }
    if request.method != 'POST':
        return render(request, 'SecureBank/login.html', args)
    else:
        # print("User: ", request.user.email)
        username = get_value(request.POST, 'username')
        password = get_value(request.POST, 'password')
        print(username)
        user = authenticate(request, username=username, password=password)
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        print("User == None", user is None)
        if user is not None and result['success']:
            login(request, user)
            if (user.is_staff):
                return redirect('/admin/') #change "user" accordingly for internal user
            else:
                return redirect('user')
            messages.success(request, 'New comment added with success!')
        else:
            args['wrong_credentials'] = True
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return render(request, 'SecureBank/login.html', args)

@login_required()
@external_user_required()
def logout_user(request):
    # if request.method == 'POST':
    logout(request)
    return HttpResponseRedirect('login')
    #else:
    #return HttpResponse('click on button first to logout')


@login_required()
@external_user_required()
def fundtransfer(request):
    args = {
        'user': request.user.username,
        'error': '',
        'accounts': request.user.bankuser.account_set.all() # List of accounts that user have
    }
    # TODO: Need to get all account of the user and show in the UI
    if request.method != 'POST':
        return render(request, 'SecureBank/funds_transfer.html', args)
    SenderAccountNumber = get_value(request.POST, 'funds_transfer_user_account')
    BeneficiaryAccountNumber = get_value(request.POST, 'funds_transfer_beneficiary_account')
    Amount = get_value(request.POST, 'funds_transfer_amount')
    print("Input entered by user", SenderAccountNumber, BeneficiaryAccountNumber, Amount)
    try:
        transaction = Transaction.Create(request.user, SenderAccountNumber, BeneficiaryAccountNumber, Amount)
    except SecureBankException as b:
        args['error'] = b.args
        print(b.args)
        return render(request, 'SecureBank/funds_transfer.html', args)
    print(request.user.bankuser.generateOTP())
    return redirect("transaction_confirmation", transaction_id=transaction.id)

@login_required()
@external_user_required()
def fundcredit(request):
    args = {
        'user': request.user.username,
        'error': '',
        'accounts': request.user.bankuser.account_set.all() # List of accounts that user have
    }
    # TODO: Need to get all account of the user and show in the UI
    if request.method != 'POST':
        return render(request, 'SecureBank/fund_credit.html', args)
    SenderAccountNumber = get_value(request.POST, 'funds_credit_user_account')
    Amount = get_value(request.POST, 'funds_credit_amount')
    print("Input entered by user for Credit", SenderAccountNumber , Amount)
    try:
        transaction = Transaction.CreateCredit(request.user, SenderAccountNumber, Amount)
    except SecureBankException as b:
        args['error'] = b.args
        print(b.args)
        return render(request, 'SecureBank/fund_credit.html', args)
    return redirect("user")

@login_required()
@external_user_required()
def funddebit(request):
    args = {
        'user': request.user.username,
        'error': '',
        'accounts': request.user.bankuser.account_set.all() # List of accounts that user have
    }
    # TODO: Need to get all account of the user and show in the UI
    if request.method != 'POST':
        return render(request, 'SecureBank/fund_debit.html', args)
    SenderAccountNumber = get_value(request.POST, 'funds_debit_user_account')
    Amount = get_value(request.POST, 'funds_debit_amount')
    print("Input entered by user For debit", SenderAccountNumber , Amount)
    try:
        transaction = Transaction.CreateDebit(request.user, SenderAccountNumber, Amount)
    except SecureBankException as b:
        args['error'] = b.args
        print(b.args)
        return render(request, 'SecureBank/fund_debit.html', args)
    return redirect("user")


@login_required
@external_user_required()
def transaction_confirmation(request, transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    args = {
        'user': request.user,
        'tid': transaction_id,
        'error': '',
    }
    if request.method != 'POST':
        return render(request, 'SecureBank/confirm_transaction.html', args)
    otp = get_value(request.POST, 'transaction_otp')
    print(otp)
    try:
        # Need to verify otp
        transaction.verify_otp(otp)
    except SecureBankException as e:
        args['error'] = e.args
        print(args['error'])
        return render(request, 'SecureBank/confirm_transaction.html', args)
    return redirect('user')



@login_required()
@external_user_required()
def profile(request):
    args = {
        'user': request.user.username
    }
    return render(request, 'SecureBank/edit_profile.html', args)


@login_required()
@external_user_required()
def home_external_user(request):
    args = {
        'user': request.user.username,
        'accounts': request.user.bankuser.account_set.all(),
        'totalBalance':''
    }
    balance =0
    for account in args['accounts']:
        balance =balance + account.Balance
    print(balance)
    args['totalBalance'] = balance
    print(args['totalBalance'])
    return render(request, 'SecureBank/summary.html', args)


@login_required()
@internal_user_required()
def home_internal_user(request):
    args = {
        'user': request.user.username,
        'transactions': Transaction.objects.all()
    }
    print('trasaction',args['transactions'])
    return render(request, 'SecureBank/transaction_summary.html', args) #change "summary.html" accordingly for internal user

@login_required()
@internal_user_required()
def authorize_transaction(request):
    args = {
        'user': request.user.username,
        'transactions': ''
    }
    try:
        args['transactions']=Transaction.objects.filter(Status='A')
    except:
        args['transactions']=None
    print(args['transactions'])
    if request.method != 'POST':
        return render(request, 'SecureBank/authorize_transaction.html',args)  # change "summary.html" accordingly for internal user

    transaction_id = get_value(request.POST, 'transaction')
    optionSelected = get_value(request.POST, 'transaction__approve_options')
    print('option', optionSelected)

    try:
        transaction = Transaction.objects.filter(id=transaction_id)
    except:
        args['error'] = 'Error in Transaction request!!'
        return render(request, 'SecureBank/authorize_transaction.html', args)

    if not len(transaction) == 0:
        transaction = transaction[0]
        print('transaction', transaction)
        if optionSelected == "Approve":
            status = transaction.approve_transaction()
            print("Status",status)
        elif optionSelected == "Reject":
            status = transaction.reject_transaction()
            print("Status", status)
        else:
            args['error']="Wrong Option!!"
        return redirect('/admin/')
    return render(request, 'SecureBank/authorize_transaction.html', args)  # change "summary.html" accordingly for internal user

