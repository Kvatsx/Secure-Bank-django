# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from SecureBank.utils import getArgumentsValues

# Create your views here.
def index(request):
    # name = 'Kaustav Vats'

    # args = {'myName': name}
    return render(request, 'SecureBank/login.html')
    # return redirect("loginView")

def loginView(request):
    if request.method != 'POST':
        return render(request, 'SecureBank/login.html')

    username = getArgumentsValues(request.POST, 'username')
    password = getArgumentsValues(request.POST, 'password')
    args = {'Username': username}
    print("Username: ", username)
    # userObject = authenticate(request, username = username, password = password)
    return render(request, 'SecureBank/dashboard.html', args)

