from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from accounts import models as finance
import json
import ast
# Create your views here.
def dashboard(request):
    username=request.user.username
    user_financials = finance.Financials.objects.get(user = username)
    stocks_owned = ""    
    stocks_owned = user_financials.stocks_owned

    if not stocks_owned:
        stocks_owned=ast.literal_eval(stocks_owned)
        return render_to_response('base/dashboard.html',{"username" : username,"stocks_owned":stocks_owned})
    
    else:
        return render_to_response('base/dashboard.html',{"username" : username})

def about(request):
    return render(request,'base/about.html')
    