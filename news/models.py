from django.db import models
from iex import Stock,reference
companies = reference.symbols()
def getStkName(stockSymbol):
    stock=companies[companies['symbol']==stockSymbol]
    return stock.iloc[0]['name']
    