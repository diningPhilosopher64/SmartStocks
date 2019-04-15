from django.shortcuts import render_to_response
from django.http import HttpResponse
from iex import Stock
from . import models
# Create your views here.
def stocknews(request,stockSymbol):
    return render_to_response('news/stocknews.html',
    {"stocknews":Stock(stockSymbol).news(last=10),"stockname":models.getStkName(stockSymbol)})
