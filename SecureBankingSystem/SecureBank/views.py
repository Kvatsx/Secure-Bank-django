# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib
import json
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from SecureBank.utils import get_value
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
# @login_required()
def index(request):
    return redirect('login')

def login_user(request):

    args = {
        'wrong_credentials' : False
    }
    if request.method != 'POST':
        return render(request, 'SecureBank/login.html', args)
    else:
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

        print(user is None)
        if user is not None and result['success']:
            login(request, user)
            if (user.is_staff):
                return redirect('home_internal_user')
            else:
                return redirect('home_external_user')
            messages.success(request, 'New comment added with success!')
        else:
            args['wrong_credentials'] = True
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return render(request, 'SecureBank/login.html', args)

@login_required()
def logout_user(request):
    # if request.method == 'POST':
    logout(request)
    return redirect('login')
    #else:
    #return HttpResponse('click on button first to logout')

@login_required()
def home_external_user(request):
    args = {
        'user': request.user.username
    }
    return render(request, 'SecureBank/home_external.html', args)


@login_required()
def fundtransfer(request):
    args = {
        'user': request.user.username
    }
    return render(request, 'SecureBank/funds_transfer.html', args)

@login_required()
def profile(request):
    args = {
        'user': request.user.username
    }
    return render(request, 'SecureBank/edit_profile.html', args)

@login_required()
def home_internal_user(request):
    args = {
        'user': request.user.username
    }
    return render(request, 'SecureBank/summary.html', args)
