# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    name = 'Kaustav Vats'

    args = {'myName': name}
    return render(request, 'SecureBank/login.html', args)