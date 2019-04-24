from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Financials
from base import views as base_views

from .forms import RegisterUser

# Create your views here.


def index(request):
    auth.logout(request)
    form = AuthenticationForm()    
    return render(request, 'accounts/home.html',{"form":form})

def login(request):
     if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return redirect(base_views.dashboard)
     else:
         form = AuthenticationForm()
     return render(request, 'accounts/login.html',{"form":form})

def all_users(request):
    users_list = User.objects.all()

    context ={"objects": users_list}
    return render(request, 'accounts/users_list.html',context)


def user_details(request): 

    user = User.objects.get(username= auth.get_user(request))       

    print(user.first_name)
    context = {"user":user}    
    return render(request,'accounts/user_detail.html',context)



def edit(request,username):
    print(username)
    return

def register(request):     

    if request.method == "POST":
        form = RegisterUser(request.POST)
        if form.is_valid():
            # current_user = request.user
            print("\n\n\n\n, Hello world \n\n\n")
            # balance=form.cleaned_data['balance'] 
            # account_num=form.cleaned_data['account_num']
            # user_financials = Financials(user= current_user,stocks_owned="",account_num=account_num,balance=balance)            
            form.save()
            # user_financials.save()

        return render(request, 'accounts/login.html')

    else:
        form = RegisterUser()   

    context = {"form":form}
    return render(request, 'accounts/register.html',context)
