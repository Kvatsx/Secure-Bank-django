from django.contrib.auth.decorators import login_required
from SecureBank.utils import get_value
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

@login_required()
def home_internal_user(request):
    args = {
        'user': request.user.username
    }
    return render(request, 'SecureBank/summary.html', args) #change "summary.html" accordingly for internal user