from django.shortcuts import render_to_response
from django.http import HttpResponse
from iex import Stock
from . import models
import json
# Create your views here.
def stocknews(request,stockname):
    return render_to_response('news/stocknews.html',
    {"stocknews":Stock(models.getSymbol(stockname)).news(last=10),"stockname":stockname})
