from django.db import models
import json
def getSymbol(stockname):
    with open('news/symbols.txt') as json_file: 
        stocks = json.load(json_file)
    for stock in stocks:
        if  str(stock['name']).find(stockname)!=-1:return str(stock['symbol'])
    return None