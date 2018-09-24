from django.shortcuts import render,redirect,reverse
from accounts.models import user
from accounts.forms import loginForm
# Create your views here.
from accounts.utils import getArgumentsValues
def home(request):
    return render(request, 'accounts/login.html')
    # return reverse('loginInput')
     # return redirect('loginInput')


def loginInput(request):
    # if request.method != 'POST':
    #     return render(request, 'accounts/login.html')
    # if request.method == 'POST':

    # form = loginForm(request.POST)
    # if form.is_valid():
    print("yoooo")
    name = getArgumentsValues(request.POST, 'username')
    password = getArgumentsValues(request.POST, 'password')
    # name = request.POST
    # password = request.POST
    a = user.objects.filter(username=name).count()
    # print(a)
    # print(name)
    # print(password)
    if a > 0:
        # print(user.objects.get(username=name).getPass)
        # print(password)
        if user.objects.get(username=name).getPass == password:
            print("Logged in")
        else:
            print("Invalid username or password")
    else:
        print("Invalid username or password")
    # userobj = user(username=name, password=password)
    # userobj.save();
    return render(request,'accounts/login.html')