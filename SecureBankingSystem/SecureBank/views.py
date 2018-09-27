# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.http import HttpResponse

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if(user.is_staff):
                return redirect('home_internal_user')
            else:
                return redirect('home_external_user')
    else:
        form = AuthenticationForm()
    return render(request, 'SecureBank/login.html', {'form':form})

@login_required()
def logout_user(request):
    # if request.method == 'POST':
    logout(request)
    return redirect('login')
    #else:
    #return HttpResponse('click on button first to logout')

@login_required()
def home_external_user(request):
    return render(request, 'SecureBank/home_external.html',{'user':request.user.username})

@login_required()
def home_internal_user(request):
    return render(request, 'SecureBank/home_internal.html',{'user':request.user.username})